import os
import logging
from typing import List, Optional, Any

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    QueryBundle,
    PromptTemplate,
    get_response_synthesizer
)
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.retrievers import VectorIndexAutoRetriever, VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.vector_stores.types import MetadataInfo, VectorStoreInfo
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore

# Configuration
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6343")
COLLECTION_NAME = "jumia_v2"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Modèles
llm = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
embed_model = OpenAIEmbedding(api_key=OPENAI_API_KEY)

class JumiaReRanker(BaseNodePostprocessor):
    """
    Re-ranker personnalisé utilisant le trust_score et le value_for_money_score (PBI-301).
    """
    def _postprocess_nodes(
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle] = None
    ) -> List[NodeWithScore]:
        if not nodes:
            return nodes
            
        logger.info(f"Re-ranking {len(nodes)} nodes...")
        for node_with_score in nodes:
            metadata = node_with_score.node.metadata
            trust = float(metadata.get("trust_score", 0.0))
            vfm = float(metadata.get("value_for_money_score", 0.0))
            
            # Normalisation et pondération (0-1)
            score_boost = (trust / 5.0) * 0.4 + (vfm / 10.0) * 0.6
            
            # On combine avec le score de similarité original
            original_score = node_with_score.score if node_with_score.score is not None else 0.0
            node_with_score.score = (original_score * 0.5) + (score_boost * 0.5)
            
            name = metadata.get('name', 'N/A')
            logger.info(f"  - {name[:30]}... | Trust: {trust} | VFM: {vfm} | Final: {node_with_score.score:.4f}")
            
        nodes.sort(key=lambda x: x.score if x.score is not None else 0.0, reverse=True)
        return nodes

def get_rag_engine(use_auto_retriever: bool = True):
    """
    Configure le moteur RAG. Si use_auto_retriever est False, utilise un retriever standard.
    """
    client = QdrantClient(url=QDRANT_URL)
    vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

    if use_auto_retriever:
        vector_store_info = VectorStoreInfo(
            content_info="Catalogue de produits Jumia",
            metadata_info=[
                MetadataInfo(name="brand", type="str", description="Marque du produit"),
                MetadataInfo(name="price_numeric", type="float", description="Prix actuel en Dhs"),
                MetadataInfo(name="category_source", type="str", description="Catégorie simplifiée (ex: smartphones, informatique)"),
                MetadataInfo(name="value_for_money_score", type="float", description="Score qualité-prix (0-10)"),
                MetadataInfo(name="trust_score", type="float", description="Score de confiance (0-5)"),
            ],
        )
        retriever = VectorIndexAutoRetriever(
            index,
            vector_store_info=vector_store_info,
            similarity_top_k=5,
            verbose=True
        )
    else:
        retriever = VectorIndexRetriever(index=index, similarity_top_k=5)

    system_prompt = (
        "Tu es 'Jumia Oral Assistant', un personal shopper expert au Maroc. "
        "Ton ton est amical, bilingue (Darija/Français) et professionnel. "
        "Mrehba, Besseha, Chouf sont tes expressions favorites. "
        "Justifie tes choix avec les scores de confiance et rapport qualité-prix."
    )
    
    llm_with_persona = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, system_prompt=system_prompt)
    response_synthesizer = get_response_synthesizer(llm=llm_with_persona, response_mode=ResponseMode.COMPACT)

    return RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[JumiaReRanker()]
    )

def expand_query_darija(query: str) -> List[str]:
    prompt = PromptTemplate(
        "Transforme cette requête (Darija/Français) en 3 variantes techniques en Français.\n"
        "Requête: {query}\n"
        "Variantes:"
    )
    response = llm.complete(prompt.format(query=query))
    lines = [l.strip().lstrip("123. -\"") for l in response.text.strip().split("\n") if l.strip()]
    return lines

class MultiQueryAutoRAG:
    def __init__(self):
        self.auto_engine = get_rag_engine(use_auto_retriever=True)
        self.base_engine = get_rag_engine(use_auto_retriever=False)
        
    def query(self, user_query: str):
        logger.info(f"Requête: {user_query}")
        variantes = expand_query_darija(user_query)
        
        try:
            response = self.auto_engine.query(user_query)
            if not response.source_nodes:
                raise ValueError("No results from auto-retriever")
        except Exception as e:
            logger.warning(f"Auto-Retriever failed or empty ({e}). Falling back to base engine...")
            # Fallback sur le moteur de base avec la meilleure variante
            response = self.base_engine.query(variantes[0] if variantes else user_query)
            
        return response

if __name__ == "__main__":
    rag = MultiQueryAutoRAG()
    tests = [
        "Bghit chi laptop m3lem b a9al mn 5000 dh",
        "Chi smartphone Samsung kbiira fih l-batterie",
        "Meilleure crème pour le visage hydratante",
        "Bghit chi hwayj dyal l-sport (chaussures)",
        "Chi bouilloire tkon rkhisa"
    ]
    for t in tests:
        print(f"\n>>> TEST: {t}")
        print(rag.query(t))
