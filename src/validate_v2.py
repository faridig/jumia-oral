import asyncio
import json
import os
import logging
from src.scraper import scrape_products

# Configuration du logging pour la validation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def validate_v2():
    # Sélection de 5 URLs représentatives de différentes catégories (même si ici on est surtout sur Jumia Informatique/Tech)
    # On va essayer de diversifier selon les titres
    urls = [
        "https://www.jumia.ma/dell-pc-portable-latitude-7480-intel-core-i5-ram-8go-256go-ssd-remis-a-neuf-62061710.html", # Laptop
        "https://www.jumia.ma/generic-souris-verticale-sans-fil-triple-connexion-2-modes-bluetooth-cle-2.4ghz-rechargeable-dpi-reglable-optique-sans-fil-5-boutons-pour-ordinateur-portable-pc-mac...-66416929.html", # Accessoire
        "https://www.jumia.ma/imprimante-couleur-mfp-178nw-laser-3-en-1-a4-usb-2.0fast-ethernetwi-fi-hp-mpg1429247.html", # Imprimante
        "https://www.jumia.ma/generic-table-dappoint-en-forme-de-c-avec-roulettes-table-de-lit-table-de-chevet-petite-table-basse-economie-despace-domestique-portable-67434568.html", # Mobilier/Accessoire
        "https://www.jumia.ma/hy-510-pate-thermique-gris-pour-refroidissement-cpu-gpu-hy510-mpg1099655.html" # Consommable/Composant
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
