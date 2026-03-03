import pytest
from src.rag_engine import JumiaReRanker
from llama_index.core.schema import NodeWithScore, TextNode

def test_hard_filtering_pbi_404():
    """
    Vérifie que le re-ranker élimine les produits avec un score sémantique < 0.8 (PBI-404).
    Même si ces produits ont des scores business parfaits.
    """
    reranker = JumiaReRanker()
    
    # Node 1: Pertinence sémantique acceptable (0.85), Business faible (0)
    # Final (avant re-ranking): 0.85
    node1 = NodeWithScore(
        node=TextNode(text="Crème hydratante", metadata={"name": "Crème A", "trust_score": 0, "value_for_money_score": 0}),
        score=0.85
    )
    
    # Node 2: Pertinence sémantique trop faible (0.75), Excellent Business (1.0 boost)
    # Final (sans hard filtering): 0.75 * 0.6 + 1.0 * 0.4 = 0.45 + 0.4 = 0.85
    # Avec hard filtering: Doit être supprimé car 0.75 < 0.8
    node2 = NodeWithScore(
        node=TextNode(text="Cartouche encre", metadata={"name": "Encre B", "trust_score": 5, "value_for_money_score": 10}),
        score=0.75
    )

    # Node 3: Pertinence sémantique limite (0.8), Business faible (0)
    # Avec hard filtering: Doit rester car 0.8 >= 0.8
    node3 = NodeWithScore(
        node=TextNode(text="Crème visage", metadata={"name": "Crème C", "trust_score": 0, "value_for_money_score": 0}),
        score=0.8
    )
    
    nodes = [node1, node2, node3]
    processed_nodes = reranker._postprocess_nodes(nodes)
    
    # Vérification des noms des produits restants
    remaining_names = [n.node.metadata['name'] for n in processed_nodes]
    
    assert "Crème A" in remaining_names, "Crème A (0.7) devrait être conservée."
    assert "Crème C" in remaining_names, "Crème C (0.6) devrait être conservée (seuil inclusif)."
    assert "Encre B" not in remaining_names, "Encre B (0.5) devrait être supprimée même avec d'excellents scores business."
    assert len(processed_nodes) == 2, f"Seulement 2 produits devraient rester, trouvé {len(processed_nodes)}."

def test_hard_filtering_empty_list():
    """Vérifie que le re-ranker gère une liste vide sans erreur."""
    reranker = JumiaReRanker()
    assert reranker._postprocess_nodes([]) == []
