import asyncio
import json
import logging
import os
import math
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

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

class ProductExtractionSchema(BaseModel):
    name: str = Field(..., description="Nom complet du produit")
    current_price: float = Field(..., description="Prix actuel du produit")
    old_price: Optional[float] = Field(None, description="Ancien prix avant promotion")
    images: List[str] = Field(..., description="Liste des URLs des images (la première est l'image principale, suivies des images secondaires/galerie)")
    url: str = Field(..., description="URL de la page produit")
    technical_specs: Dict[str, str] = Field(default_factory=dict, description="Spécifications techniques (ex: Processeur, RAM, SSD)")
    rating: float = Field(0.0, description="Note du produit sur 5")
    review_count: int = Field(0, description="Nombre total d'avis")
    review_summary: str = Field("", description="Résumé synthétique des points forts et faibles")

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
        schema=ProductExtractionSchema.model_json_schema(),
        extraction_type="schema",
        instruction="Extract all product details from the page. For prices, use numbers only. If a value is missing, use null or default. Technical specs should be a dictionary of key features. IMPORTANT: Capture the main product image URL AND all secondary image URLs from the gallery/thumbnails into the 'images' list.",
        verbose=True
    )
    
    browser_config = BrowserConfig(headless=True)
    run_config = CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        cache_mode=CacheMode.BYPASS
    )

    results = []
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        target_urls = urls[:limit]
        logger.info(f"Starting LLM extraction for {len(target_urls)} products...")
        
        for i, url in enumerate(target_urls):
            logger.info(f"Scraping {i+1}/{len(target_urls)}: {url}")
            try:
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

                    data['url'] = url
                    data['trust_score'] = calculate_trust_score(
                        float(data.get('rating') or 0.0), 
                        int(data.get('review_count') or 0)
                    )
                    
                    results.append(data)
                    logger.info(f"Successfully scraped: {data.get('name', 'Unknown')} (Score: {data['trust_score']})")
                    
                    # Sauvegarde incrémentale
                    path = save_to_markdown(data)
                    logger.info(f"Saved markdown to {path}")
                else:
                    logger.error(f"Failed to scrape {url}: {result.error_message}")
            except Exception as e:
                logger.error(f"Error scraping {url}: {str(e)}")

    return results

def save_to_markdown(product: Dict):
    """Sauvegarde le produit au format Markdown avec Frontmatter YAML"""
    base_dir = os.getenv("SCRAPER_BASE_DIR", "data/raw/markdown/informatique")
    os.makedirs(base_dir, exist_ok=True)
    
    name = product.get('name', 'Unknown_Product')
    safe_name = "".join([c if c.isalnum() else "_" for c in name[:50]]).strip("_")
    filename = f"{safe_name}.md"
    filepath = os.path.join(base_dir, filename)
    
    images = product.get("images", [])
    main_image = images[0] if images else ""
    gallery_images = images[1:] if len(images) > 1 else []
    
    frontmatter = {
        "name": product.get("name"),
        "current_price": product.get("current_price"),
        "old_price": product.get("old_price"),
        "images": images,
        "url": product.get("url"),
        "trust_score": product.get("trust_score"),
        "rating": product.get("rating"),
        "review_count": product.get("review_count"),
        "technical_specs": product.get("technical_specs")
    }
    
    gallery_md = "\n".join([f"![Image {i+1}]({img})" for i, img in enumerate(gallery_images)])
    
    content = f"""---
{json.dumps(frontmatter, indent=2)}
---

# {product.get('name', 'Nom Inconnu')}

![Image Principale]({main_image})

## Galerie d'Images
{gallery_md if gallery_md else "Aucune image secondaire disponible."}

## Résumé des Avis
{product.get('review_summary', 'Aucun résumé disponible.')}

## Spécifications Techniques
{json.dumps(product.get('technical_specs', {}), indent=2)}

## Lien Produit
[Voir sur Jumia]({product.get('url', '#')})
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
