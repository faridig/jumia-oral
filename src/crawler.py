import asyncio
import json
import logging
import os
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

# Configuration du logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/extraction.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def crawl_jumia_urls():
    base_url = "https://www.jumia.ma/ordinateurs-accessoires-informatique/"
    all_urls = set()
    
    schema = {
        "name": "Jumia Product Links",
        "baseSelector": "article.prd",
        "fields": [
            {
                "name": "url",
                "selector": "a.core",
                "type": "attribute",
                "attribute": "href"
            }
        ]
    }
    
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    
    browser_config = BrowserConfig(headless=True)
    run_config = CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for page in range(1, 11):
            url = f"{base_url}?page={page}" if page > 1 else base_url
            logger.info(f"Crawling page {page}: {url}")
            
            try:
                result = await crawler.arun(url=url, config=run_config)
                
                if result.success:
                    data = json.loads(result.extracted_content)
                    page_urls = [item['url'] for item in data if item.get('url')]
                    
                    # Ensure full URLs
                    full_urls = [
                        u if u.startswith('http') else f"https://www.jumia.ma{u}" 
                        for u in page_urls
                    ]
                    
                    before_count = len(all_urls)
                    all_urls.update(full_urls)
                    logger.info(f"Page {page}: Extracted {len(full_urls)} URLs. Unique so far: {len(all_urls)}")
                else:
                    logger.error(f"Failed to crawl page {page}: {result.error_message}")
            
            except Exception as e:
                logger.error(f"Exception on page {page}: {str(e)}")

    # Sauvegarde des résultats
    os.makedirs("data/raw", exist_ok=True)
    output_path = "data/raw/product_urls.json"
    with open(output_path, "w") as f:
        json.dump(list(all_urls), f, indent=4)
    
    # Résumé final
    summary = {
        "category": "informatique",
        "pages_crawled": 10,
        "total_urls_extracted": len(all_urls),
        "output_file": output_path
    }
    with open("data/extraction_summary.json", "w") as f:
        json.dump(summary, f, indent=4)
        
    logger.info(f"Crawling finished. Total unique URLs: {len(all_urls)}")

if __name__ == "__main__":
    asyncio.run(crawl_jumia_urls())
