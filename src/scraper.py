import asyncio
import json
import logging
import os
import math
import random
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from src.models import CategoryAgnosticProduct, SentimentAxis, SellerInfo

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

async def scrape_products(urls: List[str], limit: int = 30):
    """Scrape les détails des produits en utilisant LLM (Pure Sémantique)"""
    
    extraction_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="openai/gpt-4o-mini",
            api_token=os.getenv("OPENAI_API_KEY")
        ),
        schema=CategoryAgnosticProduct.model_json_schema(),
        extraction_type="schema",
        instruction=(
            "Extract product data into the CategoryAgnosticProduct schema for a LAPTOP (Notebook).\n"
            "1. core_metadata: Extract name, current_price (float), brand, images, url, and category (Notebooks).\n"
            "2. category_specs: MUST extract and normalize these fields:\n"
            "   - CPU: (ex: Intel Core i5-1135G7)\n"
            "   - RAM: (ex: 16GB DDR4)\n"
            "   - SSD: (ex: 512GB NVMe)\n"
            "   - GPU: (ex: Intel Iris Xe or NVIDIA RTX 3050)\n"
            "   - Screen: (ex: 15.6\" FHD IPS)\n"
            "   - Condition: (Neuf or Renewed/Reconditionné)\n"
            "3. sentiment_analysis: Focus on technical Rationale for Performance, Build Quality, and Display. NO NUMERIC SCORES.\n"
            "IMPORTANT: Prices and technical specs MUST be accurate. If a spec is not found, use 'N/A'."
        ),
        verbose=True
    )
    
    browser_config = BrowserConfig(headless=True)
    
    # JavaScript pour les interactions complexes (Avis + Scroll pour images)
    js_code = """
    (async () => {
        const sleep = (ms) => new Promise(r => setTimeout(r, ms));
        
        // 1. Nettoyage initial (popups)
        document.querySelectorAll('section.pop, .osh-popup-overlay, #newsletter-popup').forEach(p => p.remove());

        // 2. Scroll pour charger les images (lazy-loading)
        window.scrollBy(0, 500);
        await sleep(500);
        window.scrollBy(0, -500);
        await sleep(500);

        // 3. Expansion des avis
        const reviewsLink = Array.from(document.querySelectorAll('a, button, span')).find(el => 
            el.textContent.toLowerCase().includes('commentaires') || 
            el.textContent.toLowerCase().includes('avis')
        );
        
        if (reviewsLink) { 
            reviewsLink.scrollIntoView();
            reviewsLink.click(); 
            await sleep(1000); 
        }

        const seeMoreBtn = Array.from(document.querySelectorAll('a, button')).find(el => 
            el.textContent.toLowerCase().includes('voir plus') || 
            el.textContent.toLowerCase().includes('see all')
        );
        if (seeMoreBtn) { 
            seeMoreBtn.scrollIntoView();
            seeMoreBtn.click(); 
            await sleep(1500); 
        }
        
        // Retourner en haut pour s'assurer que les images principales sont visibles
        window.scrollTo(0, 0);
        await sleep(500);
    })();
    """

    results = []
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        target_urls = urls[:limit]
        logger.info(f"Starting LLM extraction for {len(target_urls)} products with review expansion...")
        
        for i, url in enumerate(target_urls):
            logger.info(f"Scraping {i+1}/{len(target_urls)}: {url}")
            try:
                # Politesse (Rate Limiting) - Pause entre chaque produit
                if i > 0:
                    pause = random.uniform(1, 3)
                    logger.info(f"Rate Limiting: pause de {pause:.2f}s...")
                    await asyncio.sleep(pause)

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
                    
                    final_data = product_obj.model_dump()
                    results.append(final_data)
                    logger.info(f"Successfully scraped: {product_obj.core_metadata.name}")
                    
                    # Sauvegarde incrémentale
                    path = save_to_markdown(final_data)
                    logger.info(f"Saved markdown to {path}")
                else:
                    logger.error(f"Failed to scrape {url}: {result.error_message}")
            except Exception as e:
                logger.error(f"Error scraping {url}: {str(e)}")

    return results

def save_to_markdown(product: Dict):
    """Sauvegarde le produit au format Markdown avec Frontmatter YAML (Neutralité Technique)"""
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
        "seller_info": product.get("seller_info")
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
    
    sentiment_md = "\n".join([f"- **{s['axis']}**: {s['rationale']}" for s in product.get('sentiment_analysis', [])])
    
    content = f"""---
{json.dumps(frontmatter, indent=2)}
---

# {core.get('name', 'Nom Inconnu')}

![Image Principale]({main_image})

## Galerie d'Images
{gallery_md if gallery_md else "Aucune image secondaire disponible."}

## Analyse de Sentiment
{sentiment_md if sentiment_md else "Pas d'analyse de sentiment disponible."}

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

    # Ingestion des 20 articles suivants (PBI-2000)
    await scrape_products(urls[10:30], limit=20)

if __name__ == "__main__":
    asyncio.run(main())
