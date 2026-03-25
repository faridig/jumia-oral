import os
import logging
from typing import List, Optional, Any, Set

import phoenix as px
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from dotenv import load_dotenv

# Initialisation Phoenix (Observabilité PBI-1306)
if os.getenv("PHOENIX_ENABLED", "true").lower() == "true":
    px.launch_app()
    from phoenix.otel import register
    register(project_name="Jumia-Oral-RAG")
    LlamaIndexInstrumentor().instrument()

from qdrant_client import QdrantClient
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    QueryBundle,
    PromptTemplate,
    Response,
    get_response_synthesizer
)
from llama_index.core.base.response.schema import RESPONSE_TYPE
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.retrievers import VectorIndexAutoRetriever, VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.vector_stores.types import MetadataInfo, VectorStoreInfo, MetadataFilters, MetadataFilter, FilterOperator
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
llm = OpenAI(model="gpt-4o", api_key=OPENAI_API_KEY, temperature=0.0)
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
        # Configuration des métadonnées pour l'Auto-Retriever (Usage Mapping PBI-1102)
        vector_store_info = VectorStoreInfo(
            content_info="Catalogue Jumia Maroc (Notebooks). Contient des specs techniques (CPU, RAM, SSD) et l'état du produit.",
            metadata_info=[
                MetadataInfo(name="brand", type="str", description="Marque du laptop (ex: HP, DELL, Lenovo)"),
                MetadataInfo(name="price_numeric", type="float", description="Prix en Dhs"),
                MetadataInfo(name="ram", type="int", description="Quantité de RAM en Go (ex: 8, 16, 32). Pour les besoins 'études', viser >= 8Go. Pour le 'gaming' ou 'montage', viser >= 16Go."),
                MetadataInfo(name="ssd", type="int", description="Capacité du SSD en Go (ex: 256, 512, 1024)."),
                MetadataInfo(name="condition", type="str", description="État du produit (ex: 'Neuf', 'Remis à Neuf')"),
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

    # Persona "Compagnon" (Rigueur Absolue & Darija-Native - PBI-1103)
    system_prompt = (
        "Tu es le 'Compagnon Notebook Jumia', un conseiller expert en PC portables au Maroc. "
        "TON DEVOIR SUPRÊME : Être factuellement IRREPROCHABLE et parler un DARIJA MAROCAIN AUTHENTIQUE. "
        "CONSIGNES DE LANGUE (OBLIGATOIRE) : "
        "1. RÉPONSE DARIJA-NATIVE : Réponds EXCLUSIVEMENT en Darija marocain naturel (sauf pour les termes techniques spécifiques CPU, GPU, RAM). INTERDICTION d'utiliser du Fusha (Arabe classique) ou du Français traduit mot-à-mot. "
        "2. GLOSSAIRE DARIJA-TECH : Utilise impérativement ces termes : "
        "   - Rapide/Puissant -> 'madi' (ex: 'Had l-PC madi bzaaf') "
        "   - Excellent/Top -> 'mkhyr' "
        "   - Très rapide/Au top -> 'tayra' "
        "   - Fluidité/Rapidité -> 'ra9a' "
        "3. ONBOARDING VOCAL (PBI-1103.3) : Si l'utilisateur te salue (Salam, Mrehba, etc.), souhaite-lui la bienvenue et précise-lui EXPLICITEMENT qu'il peut envoyer des messages VOCAUX en Darija pour poser ses questions. "
        "CONSIGNES DE CONTENU : "
        "1. PROPOSITION DOUBLE : Propose SYSTÉMATIQUEMENT 2 options (PC portables) à l'utilisateur pour lui donner le choix. Si un seul produit correspond, cherche une alternative proche. "
        "2. NOM COMPLET : Cite TOUJOURS le NOM COMPLET du produit tel qu'il apparaît dans le contexte Jumia (ex: 'HP Elitebook X360 G2'). "
        "3. STRUCTURE FACT-FIRST : Réponds à la question technique (Prix, RAM, CPU, GPU, Écran) dès la PREMIÈRE PHRASE en Darija. Tu DOIS inclure TOUTES les spécifications techniques importantes trouvées dans le contexte. "
        "4. LIENS : Termine par le lien Jumia [Voir sur Jumia](URL)."
    )
    
    llm_with_persona = OpenAI(model="gpt-4o", api_key=OPENAI_API_KEY, system_prompt=system_prompt, temperature=0.0)
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
        "1. CONSERVE impérativement les noms de modèles, marques et numéros présents dans la requête originale. INTERDICTION d'ajouter des références techniques (modèles, CPU) non mentionnées par l'utilisateur.\n"
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
        
    def query(self, user_query: str) -> RESPONSE_TYPE:
        logger.info(f"User Query: {user_query}")
        
        # 1. Expansion Sémantique (Hybridé)
        variantes = expand_query_darija(user_query)
        # On garde la query originale comme pivot central
        hybrid_query = f"{user_query} {' '.join(variantes)}"
        logger.info(f"Hybrid Query: {hybrid_query}")

        # 2. Enrichissement d'intention (Automatisé par VectorIndexAutoRetriever)
        enriched_query = user_query
        
        try:
            # Tentative via Auto-Retriever
            response = self.auto_engine.query(enriched_query)
            # Validation de la pertinence (PBI-2000: Robustesse)
            if not response.source_nodes:
                 raise ValueError("Résultat Auto-Retriever vide")
        except Exception as e:
            logger.warning(f"Auto-Retriever Fallback ({e}). Tentative via Base Engine...")
            # Fallback sur le Base Engine avec la Hybrid Query
            response = self.base_engine.query(hybrid_query)
            
        # 3. Fallback d'alternatives si toujours rien (PBI-2000: Persona Compagnon)
        if not response.source_nodes:
            logger.info("Aucun match exact. Recherche d'alternatives pour le client...")
            response = self.base_engine.query("notebook portable laptop")

        if not response.source_nodes:
            return Response(
                response="Sm7 lya, had l-produit ba9i madiyoroch f stock l-youm. Chouf chi 7aja khora?",
                source_nodes=[]
            )

        # Synthèse finale avec le prompt "Compagnon" (Garantit les 2 options)
        response = self.auto_engine._response_synthesizer.synthesize(
            query=user_query,
            nodes=response.source_nodes[:5] # On donne du choix pour que le Persona sélectionne les 2 meilleures options
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
