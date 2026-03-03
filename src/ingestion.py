import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding

# Configuration
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6343")
COLLECTION_NAME = "jumia_v2" # As specified in PBI-201
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def extract_metadata_from_markdown(file_path: Path) -> tuple[Dict[str, Any], str]:
    """
    Extrait le frontmatter JSON et le corps du document Markdown.
    """
    content = file_path.read_text(encoding="utf-8")
    
    # Séparation Frontmatter --- { JSON } --- Body
    parts = content.split("---")
    if len(parts) < 3:
        logger.warning(f"Format invalide pour {file_path}: Pas de frontmatter.")
        return {}, content

    frontmatter_raw = parts[1].strip()
    body = "---".join(parts[2:]).strip()
    
    try:
        data = json.loads(frontmatter_raw)
        
        # Mapping des champs selon PBI-201
        core = data.get("core_metadata", {})
        
        # Conversion du sentiment analysis en 'insights' pour le RAG
        sentiment = data.get("sentiment_analysis", [])
        insights = " | ".join([f"{s.get('axis')}: {s.get('rationale')}" for s in sentiment if s.get('rationale')])
        
        metadata = {
            "name": core.get("name"),
            "price_numeric": core.get("current_price"),
            "brand": core.get("brand"),
            "category": core.get("category"),
            "url": core.get("url"),
            "rating": core.get("rating"),
            "review_count": core.get("review_count"),
            "value_for_money_score": data.get("value_for_money_score"),
            "trust_score": data.get("trust_score"),
            "insights": insights,
            "category_source": file_path.parent.name, # Mapping dossier source
            "file_name": file_path.name
        }
        
        # Nettoyage des valeurs None pour Qdrant
        return {k: v for k, v in metadata.items() if v is not None}, body
        
    except json.JSONDecodeError as e:
        logger.error(f"Erreur lors du parsing JSON pour {file_path}: {e}")
        return {}, body

def ingest_products():
    """
    Pipeline d'ingestion complet vers Qdrant.
    """
    logger.info(f"Démarrage de l'ingestion vers la collection '{COLLECTION_NAME}'...")
    
    # 1. Préparation de la base vectorielle
    client = QdrantClient(url=QDRANT_URL)
    
    # Création forcée de la collection jumia_v2 si nécessaire
    collections = client.get_collections()
    if COLLECTION_NAME not in [c.name for c in collections.collections]:
        logger.info(f"Création de la collection '{COLLECTION_NAME}'...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
    
    # 2. Chargement et parsing des documents
    data_path = Path("data/raw/markdown")
    documents = []
    
    for md_file in data_path.rglob("*.md"):
        metadata, body = extract_metadata_from_markdown(md_file)
        if not metadata:
            continue
            
        doc = Document(
            text=body,
            metadata=metadata,
            excluded_llm_metadata_keys=["url", "file_name", "category_source"] # Ne pas polluer le LLM
        )
        documents.append(doc)
    
    logger.info(f"Chargement de {len(documents)} documents.")
    
    # 3. Initialisation de LlamaIndex
    vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    embed_model = OpenAIEmbedding(api_key=OPENAI_API_KEY)
    
    # 4. Création de l'index (Ingestion réelle)
    index = VectorStoreIndex.from_documents(
        documents, 
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True
    )
    
    logger.info(f"✅ Ingestion terminée avec succès dans '{COLLECTION_NAME}'.")
    return index

if __name__ == "__main__":
    ingest_products()
