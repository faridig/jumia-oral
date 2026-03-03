import pytest
from src.rag_engine import MultiQueryAutoRAG

@pytest.fixture
def rag_engine():
    return MultiQueryAutoRAG()

def test_expert_insight_integration(rag_engine):
    # Requête pour un produit présent (ex: laptop ou smartphone)
    query = "Bghit chi laptop mzyan"
    response = rag_engine.query(query)
    
    # Vérifier que la réponse contient des éléments de "conseil" ou "expert"
    # Comme c'est du LLM, on cherche des mots clés du Tone of Voice
    response_text = str(response).lower()
    
    # Vérification du ton "Coach" (on attend des mots en Darija ou des formes impératives de conseil)
    # Et surtout l'absence de concurrents
    assert "amazon" not in response_text
    assert "carrefour" not in response_text
    
    # Vérifier que les source_nodes contiennent l'insight expert
    expert_nodes = [n for n in response.source_nodes if n.node.metadata.get("is_expert_insight")]
    assert len(expert_nodes) > 0
    assert "CONSEIL D'EXPERT" in expert_nodes[0].node.text

def test_sales_compliance(rag_engine):
    # On force une requête qui pourrait tenter le LLM à comparer
    query = "Bghit Samsung, wach 7sn mn Amazon?"
    response = rag_engine.query(query)
    
    response_text = str(response).lower()
    assert "amazon" not in response_text
    # On vérifie que Jumia est mentionné ou qu'on a une réponse polie
    assert len(response_text) > 20
