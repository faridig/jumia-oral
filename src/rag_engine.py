import os
import logging
import warnings
import httpx
from typing import List, Optional, Set

import phoenix as px
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from llama_index.core import (
    VectorStoreIndex,
    QueryBundle,
    PromptTemplate,
    get_response_synthesizer
)
from llama_index.core.base.response.schema import (
    Response
)
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.retrievers import (
    VectorIndexAutoRetriever,
    VectorIndexRetriever
)
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.llms import ChatMessage
from llama_index.core.vector_stores.types import (
    MetadataInfo,
    VectorStoreInfo
)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore

# Configuration
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# Désactivation des logs verbeux
for logger_name in [
    "arize_phoenix", "openinference", "httpx", "openai", "qdrant_client"
]:
    logging.getLogger(logger_name).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Initialisation Phoenix (Observabilité PBI-1306)
if os.getenv("PHOENIX_ENABLED", "true").lower() == "true":
    try:
        px.launch_app()
        from phoenix.otel import register
        register(project_name="Jumia-Oral-RAG")
        LlamaIndexInstrumentor().instrument()
    except Exception as e:
        logger.warning(f"Phoenix n'a pas pu démarrer: {e}")

# Configuration du Silence Technique (Guidance Sprint 13)
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6343")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "jumia_products")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Modèles
llm = OpenAI(model="gpt-4o", api_key=OPENAI_API_KEY, temperature=0.0)
embed_model = OpenAIEmbedding(api_key=OPENAI_API_KEY)


class DeduplicatePostprocessor(BaseNodePostprocessor):
    """
    Dédoublonne les produits par nom (PBI-301).
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


class URLAvailabilityPostprocessor(BaseNodePostprocessor):
    """
    Vérifie en temps réel si l'URL Jumia est toujours valide (PBI-1901).
    """
    def _postprocess_nodes(
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle] = None
    ) -> List[NodeWithScore]:
        valid_nodes: List[NodeWithScore] = []

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }

        with httpx.Client(headers=headers, timeout=2.0) as client:
            for node_with_score in nodes:
                url = node_with_score.node.metadata.get("url")
                if not url:
                    logger.warning(f"Noeud sans URL trouvé: {node_with_score.node.id_}")
                    continue

                try:
                    response = client.head(url, follow_redirects=True)
                    logger.info(f"PBI-1901: {url} -> {response.status_code}")

                    if response.status_code == 404:
                        logger.warning(f"PBI-1901: Produit 404: {url}")
                    else:
                        valid_nodes.append(node_with_score)
                except httpx.RequestError as exc:
                    logger.warning(f"Erreur check URL ({url}): {exc}")
                    valid_nodes.append(node_with_score)

        return valid_nodes


def get_rag_engine(use_auto_retriever: bool = True):
    """
    Initialise le moteur de recherche.
    """
    client = QdrantClient(url=QDRANT_URL)
    vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

    if use_auto_retriever:
        vector_store_info = VectorStoreInfo(
            content_info="Catalogue Jumia Maroc (Notebooks).",
            metadata_info=[
                MetadataInfo(name="brand", type="str", description="Marque"),
                MetadataInfo(name="price_numeric", type="float", description="Prix"),
                MetadataInfo(name="ram", type="int", description="RAM"),
                MetadataInfo(name="ssd", type="int", description="SSD"),
                MetadataInfo(name="condition", type="str", description="État"),
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

    system_prompt = (
        "Tu es le 'Compagnon Notebook Jumia', un vendeur expert à Casablanca.\n"
        "TON DEVOIR : Être factuel et parler un DARIJA authentique.\n"
        "FORMAT DE SORTIE :\n"
        "[WHATSAPP] Texte minimaliste incluant TOUJOURS le lien Jumia (URL) [/WHATSAPP]\n"
        "[TTS] Texte phonétique [/TTS]"
    )

    llm_persona = OpenAI(
        model="gpt-4o",
        api_key=OPENAI_API_KEY,
        system_prompt=system_prompt,
        temperature=0.0
    )
    resp_syn = get_response_synthesizer(llm=llm_persona, response_mode=ResponseMode.COMPACT)

    return RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=resp_syn,
        node_postprocessors=[
            DeduplicatePostprocessor(),
            URLAvailabilityPostprocessor()
        ]
    )


def expand_query_darija(query: str) -> List[str]:
    """
    Enrichit la requête Darija/Français.
    """
    prompt = PromptTemplate(
        "Tu es un expert en PC portables. Analyse cette requête.\n"
        "Génère 2 variantes de recherche techniques en Français.\n"
        "Requête: {query}\n"
        "Variantes:"
    )
    response = llm.complete(prompt.format(query=query))
    lines = [
        li.strip().lstrip("123. -\"*")
        for li in response.text.strip().split("\n")
        if li.strip()
    ]
    variantes = [li for li in lines if len(li.split()) >= 1 and ":" not in li]
    return variantes[:2]


class MultiQueryAutoRAG:
    """
    Moteur RAG principal.
    """
    def __init__(self):
        self.auto_engine = get_rag_engine(use_auto_retriever=True)
        self.base_engine = get_rag_engine(use_auto_retriever=False)

    def query(self, user_query: str, chat_history: Optional[List[ChatMessage]] = None) -> Response:
        """
        Gère le RAG et la synthèse.
        """
        logger.info(f"User Query: {user_query}")
        chat_history = chat_history or []
        variantes = expand_query_darija(user_query)
        hybrid_query = f"{user_query} {' '.join(variantes)}"

        try:
            response = self.auto_engine.query(user_query)
            if not response.source_nodes:
                raise ValueError("Vide")
        except Exception:
            response = self.base_engine.query(hybrid_query)

        if not response.source_nodes:
            response = self.base_engine.query("notebook portable laptop")

        if not response.source_nodes:
            return Response(
                response="Sm7 lya, ma-lguit-ch chi bi si mnasib.",
                source_nodes=[]
            )

        history_text = "\n".join([
            f"{m.role}: {m.content}"
            for m in chat_history[-6:]
        ])
        context_query = (
            f"HISTORIQUE:\n{history_text}\n\nQUESTION:\n{user_query}"
            if history_text else user_query
        )

        response = self.auto_engine._response_synthesizer.synthesize(
            query=context_query,
            nodes=response.source_nodes[:3]
        )
        return response

    def get_retrieved_nodes(self, user_query: str) -> List[NodeWithScore]:
        """
        Récupère les nodes pertinents sans synthèse.
        """
        variantes = expand_query_darija(user_query)
        hybrid_query = f"{user_query} {' '.join(variantes)}"

        try:
            nodes = self.auto_engine.retrieve(user_query)
            if not nodes:
                raise ValueError("Vide")
        except Exception:
            nodes = self.base_engine.retrieve(hybrid_query)

        if not nodes:
            nodes = self.base_engine.retrieve("notebook portable laptop")

        return nodes[:3]


if __name__ == "__main__":
    rag = MultiQueryAutoRAG()
    print(rag.query("Bghit chi laptop m3lem"))
