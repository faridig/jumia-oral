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

class JumiaReRanker(BaseNodePostprocessor):
    """
    Re-ranker personnalisé utilisant le trust_score (40%) et le value_for_money_score (60%).
    Priorise les meilleures affaires et les vendeurs de confiance.
    Pondération : 60% pertinence sémantique / 40% scores business (PBI-401).
    Hard-Filtering : Élimine les produits avec une similarité < 0.7 (Assoupli pour les tests).
    """
    similarity_threshold: float = 0.7

    def _postprocess_nodes(
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle] = None
    ) -> List[NodeWithScore]:
        if not nodes:
            return nodes
            
        # PBI-404 : Hard-Filtering de pertinence sémantique
        filtered_nodes = []
        for node in nodes:
            if node.score is not None and node.score >= self.similarity_threshold:
                filtered_nodes.append(node)
            else:
                name = node.node.metadata.get("name", "N/A")
                logger.warning(f"  - Hard-Filtering (Score {node.score:.4f} < {self.similarity_threshold}): {name[:50]}")
        
        if not filtered_nodes:
            logger.warning(f"Aucun produit ne dépasse le seuil de pertinence ({self.similarity_threshold})")
            return []

        logger.info(f"Re-ranking de {len(filtered_nodes)} nodes après hard-filtering...")
        for node_with_score in filtered_nodes:
            metadata = node_with_score.node.metadata
            trust = float(metadata.get("trust_score", 0.0))
            vfm = float(metadata.get("value_for_money_score", 0.0))
            
            # Normalisation (Trust 0-5, VFM 0-10)
            score_boost = (trust / 5.0) * 0.4 + (vfm / 10.0) * 0.6
            
            # Pondération 60% pertinence sémantique / 40% scores business (PBI-401)
            original_score = node_with_score.score if node_with_score.score is not None else 0.0
            node_with_score.score = (original_score * 0.6) + (score_boost * 0.4)
            
            name = metadata.get('name', 'N/A')
            logger.info(f"  - {name[:30]}... | Trust: {trust} | VFM: {vfm} | Final: {node_with_score.score:.4f}")
            
        filtered_nodes.sort(key=lambda x: x.score if x.score is not None else 0.0, reverse=True)
        return filtered_nodes

def get_rag_engine(use_auto_retriever: bool = True):
    """
    Initialise le moteur de recherche avec les post-processors de dédoublonnage et re-ranking.
    """
    client = QdrantClient(url=QDRANT_URL)
    vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

    if use_auto_retriever:
        # Configuration des métadonnées pour l'Auto-Retriever (Laptop Specialized)
        vector_store_info = VectorStoreInfo(
            content_info="Catalogue Jumia Maroc Spécialisé PC Portables",
            metadata_info=[
                MetadataInfo(name="brand", type="str", description="Marque du produit"),
                MetadataInfo(name="price_numeric", type="float", description="Prix en Dhs"),
                MetadataInfo(name="ram", type="str", description="Quantité de mémoire vive (ex: 8Go, 16Go)"),
                MetadataInfo(name="ssd", type="str", description="Capacité de stockage SSD (ex: 256Go, 512Go)"),
                MetadataInfo(name="cpu", type="str", description="Modèle du processeur (ex: i5, i7, Ryzen 5)"),
                MetadataInfo(name="condition", type="str", description="État du PC (Neuf, Remis à neuf)"),
                MetadataInfo(name="value_for_money_score", type="float", description="Score 0-10"),
                MetadataInfo(name="trust_score", type="float", description="Score 0-5"),
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
        "4. Si l'utilisateur pose une question de budget, utilise les prix extraits pour confirmer. "
        "5. HONNÊTETÉ (PBI-402) : Pour tout produit ayant un trust_score de 0, mentionne explicitement en Darija qu'il n'a pas encore d'avis (ex: 'Chouf, had l-produit ba9i madiyoroch fih l-avis').\n"
        "6. SALES COMPLIANCE : Ne cite JAMAIS de noms de concurrents (ex: Amazon, Glovo, Carrefour) ni de prix provenant de sites externes. Concentre-toi uniquement sur les offres Jumia.\n"
        "7. TONE OF VOICE (PBI-502) : Agis comme un 'Coach' (Personal Shopper). Transforme l'info brute en conseil pratique (ex: 'Conseil dialna : diroh f s-sba7...'). Valorise les insights experts fournis.\n"
        "8. Si aucun produit n'est trouvé, réponds poliment en Darija que l'article n'est pas disponible pour le moment, sans mentionner d'autres sites."
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
        
        # PBI-602 : Détection d'intention de comparaison
        keywords = ["comparer", "lequel", "différence", "mieux", "meilleur", "meilleure", "vs", "akhtar"]
        is_comparison = any(k in user_query.lower() for k in keywords)
        
        variantes = expand_query_darija(user_query)
        logger.info(f"Search Variants: {variantes}")
        
        try:
            # Tentative via Auto-Retriever (extraction intelligente de filtres)
            response = self.auto_engine.query(user_query)
            if not response.source_nodes:
                raise ValueError("Résultat Auto-Retriever vide")
        except Exception as e:
            logger.warning(f"Auto-Retriever Fallback ({e}). Tentative via Base Engine...")
            search_query = variantes[0] if variantes else user_query
            response = self.base_engine.query(search_query)
            
        if not response.source_nodes:
            return "Sm7 lya, had l-produit ba9i madiyoroch f stock l-youm. Chouf chi 7aja khora?"

        # PBI-602 : Logique de comparaison assistée
        if is_comparison and len(response.source_nodes) >= 2:
            comparison_prompt = (
                "Tu es un expert Personal Shopper Jumia. L'utilisateur veut comparer des produits.\n"
                "Génère un tableau Markdown structuré comparant les 2 ou 3 meilleurs produits trouvés.\n"
                "Colonnes : Produit | Prix | Trust Score | Value for Money | Points Forts\n"
                "Après le tableau, ajoute une section '🎯 Verdict de l'Expert' en Darija uniquement.\n"
                "Le verdict doit être tranché et expliquer lequel est le 'meilleur' choix selon le profil.\n"
                "Données :\n{context_str}"
            )
            # On utilise le synthesizer avec ce prompt spécifique
            synthesizer = get_response_synthesizer(
                llm=llm, 
                text_qa_template=PromptTemplate(comparison_prompt),
                response_mode=ResponseMode.COMPACT
            )
            response = synthesizer.synthesize(query=user_query, nodes=response.source_nodes[:3])
            return response

        # PBI-502 : Enrichissement VFM via Expertise Externe (pour les requêtes simples)
        if response.source_nodes:


            top_node = response.source_nodes[0]
            product_name = top_node.node.metadata.get("name", "Produit")
            category = top_node.node.metadata.get("category_source", "Général")
            
            expert_insight = expert_advisor.get_expert_insight(product_name, category)
            logger.info(f"Expert Insight added: {expert_insight[:50]}...")
            
            # Injection de l'insight dans le prompt de synthèse en modifiant le texte de la réponse
            # Ou plus proprement en ajoutant un node synthétique d'expertise
            from llama_index.core.schema import TextNode, NodeWithScore
            expert_node = NodeWithScore(
                node=TextNode(
                    text=f"CONSEIL D'EXPERT (Context7) : {expert_insight}",
                    metadata={"is_expert_insight": True, "product_name": product_name}
                ),
                score=1.0 # Haute priorité
            )
            response.source_nodes.insert(0, expert_node)
            
            # Re-générer la réponse si nécessaire ? 
            # Non, LlamaIndex utilise les source_nodes pour la synthèse. 
            # Mais ici `response` contient déjà le texte généré !
            # Je dois donc appeler le synthesizer MANUELLEMENT ou intercepter AVANT.
            
            # Correction : L'appel à `query` déclenche déjà la synthèse. 
            # Je dois donc refaire la synthèse avec le nouveau node ou modifier l'engine.
            
            # Approche plus robuste : On refait la synthèse avec les nodes enrichis.
            response = self.auto_engine._response_synthesizer.synthesize(
                query=user_query,
                nodes=response.source_nodes
            )
            
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
