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

from src.expert_advisor import expert_advisor

# Configuration
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6343")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "jumia_products")
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
            content_info="Catalogue Jumia Maroc Spécialisé PC Portables (Pure Sémantique)",
            metadata_info=[
                MetadataInfo(name="brand", type="str", description="Marque du produit"),
                MetadataInfo(name="price_numeric", type="float", description="Prix en Dhs (numérique)"),
                MetadataInfo(name="ram", type="str", description="Mémoire vive. Utiliser uniquement des filtres d'égalité (ex: ram == '16Go')."),
                MetadataInfo(name="ssd", type="str", description="Stockage SSD. Utiliser uniquement des filtres d'égalité."),
                MetadataInfo(name="cpu", type="str", description="Modèle processeur. Utiliser uniquement des filtres d'égalité."),
                MetadataInfo(name="gpu", type="str", description="Carte graphique. Utiliser uniquement des filtres d'égalité."),
                MetadataInfo(name="condition", type="str", description="État du PC (Neuf, Renewed)"),
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

    # Personnalité "Compagnon Notebook" (PBI-2000)
    system_prompt = (
        "Tu es le 'Compagnon Notebook Jumia', un expert technique Personal Shopper au Maroc. "
        "Ta mission est d'aider l'utilisateur à trouver les DEUX MEILLEURS laptops selon son besoin. "
        "Tu parles en Français avec des touches de Darija (Mrehba, Besseha, Chouf, Mzyan). "
        "CONSIGNES STRICTES : "
        "1. Analyse l'intention d'usage (Gaming, Études, Montage, Bureautique). "
        "2. Propose SYSTÉMATIQUEMENT les 2 meilleures options trouvées dans le contexte. "
        "3. Pour chaque option, affiche : Nom, Prix, Specs clés (CPU/RAM/SSD) et l'URL JUMIA DIRECTE. "
        "4. Justifie ton choix uniquement par la pertinence technique (Specs vs Intention). "
        "5. Ne mentionne JAMAIS de scores numériques (Trust/VFM). Utilise les 'insights' textuels. "
        "6. Sois tranché et honnête : si un produit est mieux pour le gaming, dis-le clairement. "
        "7. Format de réponse : Présentation brève -> Option 1 -> Option 2 -> Conseil d'expert en Darija."
    )
    
    llm_with_persona = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, system_prompt=system_prompt)
    response_synthesizer = get_response_synthesizer(llm=llm_with_persona, response_mode=ResponseMode.COMPACT)

    return RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[DeduplicatePostprocessor()]
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
        
        # Mappage des intentions vers des filtres techniques (PBI-2000 Action 2)
        # On laisse l'Auto-Retriever gérer l'extraction des filtres, mais on peut enrichir la query
        enriched_query = user_query
        if any(k in user_query.lower() for k in ["gaming", "jeux", "gamer"]):
            enriched_query += " (Besoin: GPU performant, RAM >= 16Go, CPU i7 ou Ryzen 7)"
        elif any(k in user_query.lower() for k in ["études", "etudiant", "ecole", "bureautique"]):
            enriched_query += " (Besoin: Autonomie, RAM >= 8Go, i5 ou Ryzen 5, SSD)"
        elif any(k in user_query.lower() for k in ["montage", "video", "graphisme"]):
            enriched_query += " (Besoin: Écran haute qualité, RAM >= 16Go, GPU dédié)"

        variantes = expand_query_darija(user_query)
        logger.info(f"Search Variants: {variantes}")
        
        try:
            # Tentative via Auto-Retriever
            response = self.auto_engine.query(enriched_query)
            if not response.source_nodes:
                raise ValueError("Résultat Auto-Retriever vide")
        except Exception as e:
            logger.warning(f"Auto-Retriever Fallback ({e}). Tentative via Base Engine...")
            search_query = variantes[0] if variantes else enriched_query
            response = self.base_engine.query(search_query)
            
        if not response.source_nodes:
            return "Sm7 lya, had l-produit ba9i madiyoroch f stock l-youm. Chouf chi 7aja khora?"

        # Enrichissement avec l'expertise technique (Context7) si disponible
        if response.source_nodes:
            top_node = response.source_nodes[0]
            product_name = top_node.node.metadata.get("name", "Produit")
            category = top_node.node.metadata.get("category_source", "Notebooks")
            
            expert_insight = expert_advisor.get_expert_insight(product_name, category)
            
            from llama_index.core.schema import TextNode, NodeWithScore
            expert_node = NodeWithScore(
                node=TextNode(
                    text=f"GUIDE TECHNIQUE : {expert_insight}",
                    metadata={"is_expert_insight": True}
                ),
                score=1.0
            )
            # On s'assure d'avoir au moins 2 nodes de produits + 1 node expertise
            nodes_for_synthesis = response.source_nodes[:2] # Top 2 Notebooks
            nodes_for_synthesis.append(expert_node)
            
            # Synthèse finale avec le prompt "Compagnon"
            response = self.auto_engine._response_synthesizer.synthesize(
                query=user_query,
                nodes=nodes_for_synthesis
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
