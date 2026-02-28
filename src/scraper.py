import asyncio
import json
import logging
import os
import math
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from src.models import CategoryAgnosticProduct, SentimentAxis, SellerInfo, ShippingFees

load_dotenv()

# Configuration du logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/scraping.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def calculate_trust_score(rating: float, review_count: int) -> float:
    """Calcul du trust_score : (Note * 0.7) + (log10(Avis) * 0.3)"""
    if review_count <= 0:
        return round(rating * 0.7, 2)
    log_reviews = math.log10(review_count)
    score = (rating * 0.7) + (log_reviews * 0.3)
    return round(score, 2)

async def scrape_products(urls: List[str], limit: int = 5):
    """Scrape les détails des produits en utilisant LLM"""
    
    extraction_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="openai/gpt-4o-mini",
            api_token=os.getenv("OPENAI_API_KEY")
        ),
        schema=CategoryAgnosticProduct.model_json_schema(),
        extraction_type="schema",
        instruction=(
            "Extract product data into the CategoryAgnosticProduct schema.\n"
            "1. core_metadata: Extract name, current_price (float, numbers only), old_price (float, numbers only), brand, images, url, and category.\n"
            "2. category_specs: Normalize all technical specifications. Convert units to standard international formats "
            "(e.g., '8Go' or '8G' to '8 GB', '100ml' to '100 ml', '2To' to '2 TB').\n"
            "3. sentiment_analysis: Evaluate the product based on customer reviews and description across 4 axes: "
            "Performance, Design, Autonomie, and Prix. Provide a score (0-10) and a brief rationale for each.\n"
            "4. value_for_money_score: Calculate a score from 0 to 10 based on the quality/features vs price.\n"
            "5. Extract seller information and raw_review_summary.\n"
            "6. shipping_fees: Extract shipping fees. Read the line starting with 'SHIPPING_DATA' at the top of the page. "
            "It contains raw delivery info. Map it to the hubs (Casablanca, etc.) if possible. "
            "If only one price is found, assign it to Casablanca as the default.\n"
            "IMPORTANT: Be precise with normalization. Prices MUST be numbers (floats). If information is missing, use null."
        ),
        verbose=True
    )
    
    browser_config = BrowserConfig(headless=True)
    
    # JavaScript pour cliquer sur "Commentaires des clients", "Voir plus" et extraire les infos de livraison
    js_code = """
    (async () => {
        const sleep = (ms) => new Promise(r => setTimeout(r, ms));
        
        // 1. Fermer les popups intrusifs
        const popup = document.querySelector('section.pop, .osh-popup-overlay');
        if (popup) popup.remove();
        
        // 2. Chercher et cliquer sur l'onglet/lien des commentaires
        const reviewsLink = Array.from(document.querySelectorAll('a, button, span')).find(el => 
            el.textContent.toLowerCase().includes('commentaires') || 
            el.textContent.toLowerCase().includes('avis')
        );
        if (reviewsLink) {
            reviewsLink.click();
            await sleep(1000);
        }

        // 3. Chercher et cliquer sur "Voir plus" dans les avis
        const seeMoreBtn = Array.from(document.querySelectorAll('a, button')).find(el => 
            el.textContent.toLowerCase().includes('voir plus') || 
            el.textContent.toLowerCase().includes('see all')
        );
        if (seeMoreBtn) {
            seeMoreBtn.click();
            await sleep(1500);
        }

        // Interaction Logistique (PBI-130)
        const allText = document.body.innerText;
        const shippingMarker = document.createElement('div');
        shippingMarker.id = 'shipping-data-extract';
        shippingMarker.innerText = "LIVRAISON_BRUT: " + allText.substring(0, 5000); // On prend un gros bloc
        document.body.prepend(shippingMarker);
    })();
    """

    results = []
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        target_urls = urls[:limit]
        logger.info(f"Starting LLM extraction for {len(target_urls)} products with review expansion...")
        
        for i, url in enumerate(target_urls):
            logger.info(f"Scraping {i+1}/{len(target_urls)}: {url}")
            try:
                # On utilise un session_id unique pour permettre les interactions JS complexes
                session_id = f"session_{i}"
                
                # Configuration pour l'extraction avec JS
                run_config = CrawlerRunConfig(
                    extraction_strategy=extraction_strategy,
                    cache_mode=CacheMode.BYPASS,
                    js_code=js_code,
                    wait_for_images=True,
                    session_id=session_id
                )

                result = await crawler.arun(url=url, config=run_config)
                
                if result.success:
                    extracted_data = json.loads(result.extracted_content)
                    # L'extraction peut renvoyer une liste ou un objet
                    if isinstance(extracted_data, list):
                        data = extracted_data[0] if extracted_data else {}
                    else:
                        data = extracted_data
                    
                    if not data:
                        logger.warning(f"No data extracted for {url}")
                        continue

                    # Validation et post-processing
                    product_obj = CategoryAgnosticProduct(**data)
                    product_obj.core_metadata.url = url
                    
                    # Trust score calculation (using rating from core_metadata if available)
                    rating = product_obj.core_metadata.rating
                    review_count = product_obj.core_metadata.review_count
                    product_obj.trust_score = calculate_trust_score(float(rating or 0.0), int(review_count or 0))
                    
                    final_data = product_obj.model_dump()
                    results.append(final_data)
                    logger.info(f"Successfully scraped: {product_obj.core_metadata.name} (Score: {product_obj.trust_score})")
                    
                    # Sauvegarde incrémentale
                    path = save_to_markdown(final_data)
                    logger.info(f"Saved markdown to {path}")
                else:
                    logger.error(f"Failed to scrape {url}: {result.error_message}")
            except Exception as e:
                logger.error(f"Error scraping {url}: {str(e)}")

    return results

def save_to_markdown(product: Dict):
    """Sauvegarde le produit au format Markdown avec Frontmatter YAML"""
    category = product.get('core_metadata', {}).get('category')
    if category:
        category = category.lower()
    else:
        category = 'diverse'
    
    base_dir = os.path.join(os.getenv("SCRAPER_BASE_DIR", "data/raw/markdown"), category)
    os.makedirs(base_dir, exist_ok=True)
    
    name = product.get('core_metadata', {}).get('name', 'Unknown_Product')
    safe_name = "".join([c if c.isalnum() else "_" for c in name[:50]]).strip("_")
    filename = f"{safe_name}.md"
    filepath = os.path.join(base_dir, filename)
    
    core = product.get("core_metadata", {})
    images = core.get("images", [])
    main_image = images[0] if images else ""
    gallery_images = images[1:] if len(images) > 1 else []
    
    # On structure le frontmatter pour être RAG-Ready
    frontmatter = {
        "core_metadata": core,
        "category_specs": product.get("category_specs"),
        "sentiment_analysis": product.get("sentiment_analysis"),
        "value_for_money_score": product.get("value_for_money_score"),
        "trust_score": product.get("trust_score"),
        "seller_info": product.get("seller_info"),
        "shipping_fees": product.get("shipping_fees")
    }
    
    seller = product.get("seller_info", {})
    seller_md = ""
    if seller:
        seller_md = f"""
### Informations Vendeur
- **Nom**: {seller.get('name', 'N/A')}
- **Évaluation**: {seller.get('rating_percentage', 'N/A')}
- **Abonnés**: {seller.get('follower_count', 'N/A')}

#### Performance Vendeur
- **Vitesse d'expédition**: {seller.get('shipping_speed', 'N/A')}
- **Score Qualité**: {seller.get('quality_score', 'N/A')}
- **Avis Consommateurs**: {seller.get('customer_reviews_score', 'N/A')}
"""

    gallery_md = "\n".join([f"![Image {i+1}]({img})" for i, img in enumerate(gallery_images)])
    
    sentiment_md = "\n".join([f"- **{s['axis']}**: {s['score']}/10 - {s['rationale']}" for s in product.get('sentiment_analysis', [])])
    
    content = f"""---
{json.dumps(frontmatter, indent=2)}
---

# {core.get('name', 'Nom Inconnu')}

![Image Principale]({main_image})

## Galerie d'Images
{gallery_md if gallery_md else "Aucune image secondaire disponible."}

## Analyse de Sentiment
{sentiment_md if sentiment_md else "Pas d'analyse de sentiment disponible."}

**Score Rapport Qualité-Prix**: {product.get('value_for_money_score', 'N/A')}/10

## Détails du Vendeur
{seller_md if seller_md else "Informations vendeur non disponibles."}

## Résumé des Avis (Brut)
{product.get('raw_review_summary', 'Aucun résumé disponible.')}

## Spécifications Techniques (Normalisées)
{json.dumps(product.get('category_specs', {}), indent=2)}

## Lien Produit
[Voir sur Jumia]({core.get('url', '#')})
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return filepath

async def main():
    try:
        with open("data/raw/product_urls.json", "r") as f:
            urls = json.load(f)
    except FileNotFoundError:
        logger.error("product_urls.json not found. Run crawler first.")
        return

    if not urls:
        logger.error("No URLs found in product_urls.json.")
        return

    # On commence par un batch de 10 produits
    await scrape_products(urls, limit=10)

if __name__ == "__main__":
    asyncio.run(main())
