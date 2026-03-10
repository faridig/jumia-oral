import os
import logging
from typing import List, Optional, Any, Set

import phoenix as px
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from dotenv import load_dotenv

# Initialisation Phoenix (Observabilité PBI-1306)
if os.getenv("PHOENIX_ENABLED", "true").lower() == "true":
    px.launch_app()
    LlamaIndexInstrumentor().instrument()

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

# Configuration du Silence Technique (Guidance Sprint 13)
import warnings
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

# Configuration
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Désactivation des logs verbeux des bibliothèques tierces
for logger_name in ["arize_phoenix", "openinference", "httpx", "openai", "qdrant_client"]:
    logging.getLogger(logger_name).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6343")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "jumia_products")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Modèles
llm = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0.0)
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

def get_rag_engine(use_auto_retriever: bool = True):
    """
    Initialise le moteur de recherche avec les post-processors de dédoublonnage.
    """
    client = QdrantClient(url=QDRANT_URL)
    vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

    if use_auto_retriever:
        # Configuration des métadonnées pour l'Auto-Retriever (Laptop Specialized PBI-2000)
        vector_store_info = VectorStoreInfo(
            content_info="Catalogue Jumia Maroc (Notebooks). Contient des specs techniques (CPU, RAM, SSD) et l'état du produit.",
            metadata_info=[
                MetadataInfo(name="brand", type="str", description="Marque du laptop (ex: HP, DELL, Lenovo)"),
                MetadataInfo(name="price_numeric", type="float", description="Prix en Dhs"),
                MetadataInfo(name="ram", type="str", description="RAM (ex: 8GB, 16GB)"),
                MetadataInfo(name="ssd", type="str", description="Stockage (ex: 256GB, 512GB)"),
                # Condition retirée des filtres structurés car trop incohérente dans l'index (Remis à neuf vs Remis à Neuf)
            ],
        )
        retriever = VectorIndexAutoRetriever(
            index,
            vector_store_info=vector_store_info,
            similarity_top_k=5,
            llm=llm,
            verbose=True
        )
    else:
        retriever = VectorIndexRetriever(index=index, similarity_top_k=5)

    # Persona "Compagnon" (Rigueur Absolue - PBI-2000)
    system_prompt = (
        "Tu es le 'Compagnon Notebook Jumia', un conseiller expert en PC portables au Maroc. "
        "TON DEVOIR SUPRÊME : Ne jamais inventer de détails techniques. "
        "CONSIGNES : "
        "1. FIDÉLITÉ AU CONTEXTE : N'utilise QUE les informations techniques présentes dans le contexte fourni. Si une info manque (ex: modèle précis de CPU comme i5-6300U, résolution Full HD), ne l'invente pas. Reste général (ex: 'Intel Core i5') si c'est tout ce que tu as. "
        "2. RÉPONSE DIRECTE : Pour une question factuelle, donne l'information immédiatement. "
        "3. ACCUEIL & TON : Garde un ton amical avec des touches de Darija (Mrehba, Mzyan, Besseha). "
        "4. MODE CONSEIL : Propose 2 options (Option 1 / Option 2) uniquement si l'utilisateur demande un conseil ou une recherche large. "
        "5. LIENS : Ajoute toujours le lien Jumia [Voir sur Jumia](URL) pour chaque produit cité. "
        "6. INTERDICTION : Ne mentionne aucune spécification technique qui n'est pas explicitement écrite dans le texte source."
    )
    
    llm_with_persona = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, system_prompt=system_prompt, temperature=0.0)
    response_synthesizer = get_response_synthesizer(llm=llm_with_persona, response_mode=ResponseMode.COMPACT)

    return RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[DeduplicatePostprocessor()]
    )

def expand_query_darija(query: str) -> List[str]:
    """
    Enrichit la requête Darija/Français avec des termes techniques tout en préservant les références.
    """
    prompt = PromptTemplate(
        "Tu es un expert en PC portables. Analyse cette requête (Darija ou Français).\n"
        "Génère 2 variantes de recherche techniques en Français qui :\n"
        "1. CONSERVENT impérativement les noms de modèles, marques et numéros (ex: 5490, G3, i7).\n"
        "2. AJOUTENT des termes sémantiques équivalents.\n"
        "RÉPONDS SEULEMENT AVEC LES VARIANTES, UNE PAR LIGNE.\n"
        "Requête: {query}\n"
        "Variantes:"
    )
    response = llm.complete(prompt.format(query=query))
    lines = [l.strip().lstrip("123. -\"*") for l in response.text.strip().split("\n") if l.strip()]
    variantes = [l for l in lines if len(l.split()) >= 1 and ":" not in l]
    return variantes[:2]

class MultiQueryAutoRAG:
    """
    Moteur RAG principal gérant l'Auto-Retriever avec Fallback sur recherche vectorielle simple.
    """
    def __init__(self):
        self.auto_engine = get_rag_engine(use_auto_retriever=True)
        self.base_engine = get_rag_engine(use_auto_retriever=False)
        
    def query(self, user_query: str):
        logger.info(f"User Query: {user_query}")
        
        # 1. Expansion Sémantique (Hybridé)
        variantes = expand_query_darija(user_query)
        # On garde la query originale comme pivot central
        hybrid_query = f"{user_query} {' '.join(variantes)}"
        logger.info(f"Hybrid Query: {hybrid_query}")

        # 2. Enrichissement d'intention (Optionnel pour l'Auto-Retriever)
        enriched_query = user_query
        if any(k in user_query.lower() for k in ["gaming", "jeux", "gamer"]):
            enriched_query += " (Besoin: GPU performant, RAM >= 16Go)"
        elif any(k in user_query.lower() for k in ["études", "etudiant", "ecole"]):
            enriched_query += " (Besoin: Autonomie, RAM >= 8Go)"
        
        try:
            # Tentative via Auto-Retriever (Utilise la query originale enrichie d'intention)
            response = self.auto_engine.query(enriched_query)
            if not response.source_nodes:
                raise ValueError("Résultat Auto-Retriever vide")
        except Exception as e:
            logger.warning(f"Auto-Retriever Fallback ({e}). Tentative via Base Engine...")
            # Fallback sur le Base Engine avec la Hybrid Query (Original + Expansion)
            response = self.base_engine.query(hybrid_query)
            
        if not response.source_nodes:
            return "Sm7 lya, had l-produit ba9i madiyoroch f stock l-youm. Chouf chi 7aja khora?"

        # Synthèse finale avec le prompt "Compagnon"
        response = self.auto_engine._response_synthesizer.synthesize(
            query=user_query,
            nodes=response.source_nodes[:2] # Top 2 Notebooks
        )
            
        return response

if __name__ == "__main__":
    rag = MultiQueryAutoRAG()
    tests = [
        "Bghit chi laptop m3lem b a9al mn 5000 dh",
    ]
    for t in tests:
        print(f"\n>>> TEST: {t}")
        print(rag.query(t))
