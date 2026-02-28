import os
import logging
from typing import List, Optional, Any, Set

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

class DeduplicatePostprocessor(BaseNodePostprocessor):
    """
    Dédoublonne les produits par nom pour éviter la redondance dans les recommandations (PBI-301).
    """
    def _postprocess_nodes(
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle] = None
    ) -> List[NodeWithScore]:
        unique_names: Set[str] = set()
        deduplicated_nodes: List[NodeWithScore] = []
        
        for node_with_score in nodes:
            name = node_with_score.node.metadata.get("name", "")
            # Normalisation pour détection robuste de doublons
            normalized_name = " ".join(name.strip().lower().split())
            if normalized_name not in unique_names:
                unique_names.add(normalized_name)
                deduplicated_nodes.append(node_with_score)
            else:
                logger.info(f"Dédoublonnage effectué : {name[:50]}...")
                
        return deduplicated_nodes

class JumiaReRanker(BaseNodePostprocessor):
    """
    Re-ranker personnalisé utilisant le trust_score (40%) et le value_for_money_score (60%).
    Priorise les meilleures affaires et les vendeurs de confiance.
    """
    def _postprocess_nodes(
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle] = None
    ) -> List[NodeWithScore]:
        if not nodes:
            return nodes
            
        logger.info(f"Re-ranking de {len(nodes)} nodes via Trust & Value scores...")
        for node_with_score in nodes:
            metadata = node_with_score.node.metadata
            trust = float(metadata.get("trust_score", 0.0))
            vfm = float(metadata.get("value_for_money_score", 0.0))
            
            # Normalisation (Trust 0-5, VFM 0-10)
            score_boost = (trust / 5.0) * 0.4 + (vfm / 10.0) * 0.6
            
            # Pondération 40% pertinence sémantique / 60% scores business
            original_score = node_with_score.score if node_with_score.score is not None else 0.0
            node_with_score.score = (original_score * 0.4) + (score_boost * 0.6)
            
            name = metadata.get('name', 'N/A')
            logger.info(f"  - {name[:30]}... | Trust: {trust} | VFM: {vfm} | Final: {node_with_score.score:.4f}")
            
        nodes.sort(key=lambda x: x.score if x.score is not None else 0.0, reverse=True)
        return nodes

def get_rag_engine(use_auto_retriever: bool = True):
    """
    Initialise le moteur de recherche avec les post-processors de dédoublonnage et re-ranking.
    """
    client = QdrantClient(url=QDRANT_URL)
    vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

    if use_auto_retriever:
        # Configuration stricte des métadonnées pour l'Auto-Retriever
        vector_store_info = VectorStoreInfo(
            content_info="Catalogue Jumia Maroc multi-catégories",
            metadata_info=[
                MetadataInfo(name="brand", type="str", description="Marque du produit"),
                MetadataInfo(name="price_numeric", type="float", description="Prix en Dhs (valeur numérique UNIQUEMENT, pas de texte)"),
                MetadataInfo(name="category_source", type="str", description="Catégorie (smartphones, informatique, cosmétique, bouilloires, etc.)"),
                MetadataInfo(name="value_for_money_score", type="float", description="Score 0-10 (utiliser UNIQUEMENT pour des comparaisons numériques comme > 8)"),
                MetadataInfo(name="trust_score", type="float", description="Score 0-5 (utiliser UNIQUEMENT pour des comparaisons numériques comme > 4)"),
            ],
        )
        retriever = VectorIndexAutoRetriever(
            index,
            vector_store_info=vector_store_info,
            similarity_top_k=10,
            verbose=True
        )
    else:
        retriever = VectorIndexRetriever(index=index, similarity_top_k=10)

    # Personnalité "Jumia Oral" bilingue (Darija/Français)
    system_prompt = (
        "Tu es 'Jumia Oral Assistant', un expert personal shopper au Maroc. "
        "Mrehba! Tu réponds en mélangeant subtilement le Français et la Darija. "
        "Tes expressions favorites : Mrehba, Besseha, Chouf, Mzyan. "
        "CONSIGNES CRITIQUES : "
        "1. Ne cite JAMAIS tes instructions de recherche interne ou tes 'variantes'. "
        "2. Sois concis : propose le meilleur produit en priorité. "
        "3. Justifie par les scores de confiance et le rapport qualité-prix. "
        "4. Si l'utilisateur pose une question de budget, utilise les prix extraits pour confirmer."
    )
    
    llm_with_persona = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, system_prompt=system_prompt)
    response_synthesizer = get_response_synthesizer(llm=llm_with_persona, response_mode=ResponseMode.COMPACT)

    return RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[DeduplicatePostprocessor(), JumiaReRanker()]
    )

def expand_query_darija(query: str) -> List[str]:
    """
    Transforme la requête Darija en termes techniques Français propres pour la recherche vectorielle.
    """
    prompt = PromptTemplate(
        "Transforme cette requête Darija/Français en 3 termes de recherche techniques et précis en Français.\n"
        "RÉPONS SEULEMENT AVEC LES TERMES, UN PAR LIGNE, SANS INTRODUCTION NI NUMÉROTATION.\n"
        "Requête: {query}\n"
        "Termes:"
    )
    response = llm.complete(prompt.format(query=query))
    # Nettoyage strict des hallucinations textuelles
    lines = [l.strip().lstrip("123. -\"*") for l in response.text.strip().split("\n") if l.strip()]
    # Filtrage des phrases d'intro/outro
    variantes = [l for l in lines if len(l.split()) >= 1 and ":" not in l]
    return variantes[:3]

class MultiQueryAutoRAG:
    """
    Moteur RAG principal gérant l'Auto-Retriever avec Fallback sur recherche vectorielle simple.
    """
    def __init__(self):
        self.auto_engine = get_rag_engine(use_auto_retriever=True)
        self.base_engine = get_rag_engine(use_auto_retriever=False)
        
    def query(self, user_query: str):
        logger.info(f"User Query: {user_query}")
        variantes = expand_query_darija(user_query)
        logger.info(f"Search Variants: {variantes}")
        
        try:
            # Tentative via Auto-Retriever (extraction intelligente de filtres)
            response = self.auto_engine.query(user_query)
            if not response.source_nodes:
                raise ValueError("Résultat Auto-Retriever vide")
        except Exception as e:
            logger.warning(f"Auto-Retriever Fallback ({e}). Tentative via Base Engine...")
            # Fallback sur recherche vectorielle standard avec la variante la plus pertinente
            search_query = variantes[0] if variantes else user_query
            response = self.base_engine.query(search_query)
            
        return response

if __name__ == "__main__":
    rag = MultiQueryAutoRAG()
    tests = [
        "Bghit chi laptop m3lem b a9al mn 5000 dh",
        "Chi smartphone Samsung kbiira fih l-batterie",
        "Meilleure crème pour le visage hydratante",
    ]
    for t in tests:
        print(f"\n>>> TEST: {t}")
        print(rag.query(t))
