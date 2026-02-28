import asyncio
import json
import os
import logging
from src.scraper import scrape_products

# Configuration du logging pour la validation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def validate_v2():
    # Sélection de 5 URLs représentatives de différentes catégories pour DoD PBI-120
    urls = [
        "https://www.jumia.ma/dell-pc-portable-latitude-7480-intel-core-i5-ram-8go-256go-ssd-remis-a-neuf-62061710.html", # Laptop
        "https://www.jumia.ma/samsung-galaxy-a16-8gb-256gb-black-2-ans-de-garantie-65981498.html", # Smartphone
        "https://www.jumia.ma/erborian-cc-creme-a-la-centella-clair-soin-illuminateur-visage-spf-25-45-ml-67325709.html", # Cosmétique
        "https://www.jumia.ma/meuble-7-couches-pour-chaussures-etagere-de-rangement-diaphragme-anti-poussiere-porte-de-dortoir-generic-mpg1517017.html", # Bricolage/Maison
        "https://www.jumia.ma/bouilloire-electrique-elegant-18l-1500w-bg1500-kenz-mpg1460090.html" # Électroménager
    ]
    
    logger.info(f"Démarrage de la validation V2 pour {len(urls)} produits...")
    results = await scrape_products(urls, limit=5)
    
    logger.info(f"Validation terminée. {len(results)} produits scrapés.")
    
    # Vérification sommaire de la structure
    for res in results:
        name = res.get('core_metadata', {}).get('name')
        category = res.get('core_metadata', {}).get('category')
        vfm = res.get('value_for_money_score')
        sentiment = res.get('sentiment_analysis')
        
        logger.info(f"Produit: {name}")
        logger.info(f"  - Catégorie: {category}")
        logger.info(f"  - Value for Money: {vfm}")
        logger.info(f"  - Sentiment Axes: {[s['axis'] for s in sentiment] if sentiment else 'None'}")
        
    if len(results) == 5:
        logger.info("✅ Succès: 5 produits scrapés avec le nouveau format.")
    else:
        logger.warning(f"⚠️ Attention: Seulement {len(results)} produits scrapés.")

if __name__ == "__main__":
    asyncio.run(validate_v2())
