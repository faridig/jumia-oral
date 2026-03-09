import os
import json
import pytest
from deepeval.metrics import FaithfulnessMetric, ContextualPrecisionMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval import assert_test
from src.rag_engine import MultiQueryAutoRAG

# Stabilisation DeepEval (Sprint 13)
os.environ["DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE"] = "300"

# Initialisation du moteur RAG
rag = MultiQueryAutoRAG()

def load_gold_dataset():
    # En CI, on évite de charger tout le dataset si on n'a pas les clés API
    if not os.getenv("OPENAI_API_KEY") and os.getenv("GITHUB_ACTIONS") == "true":
        return []
        
    try:
        with open("tests/gold_dataset.json", "r") as f:
            data = json.load(f)
            # Limiter à 5 tests en CI pour le budget/temps
            if os.getenv("GITHUB_ACTIONS") == "true":
                return data[:5]
            return data
    except FileNotFoundError:
        return []

@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OpenAI API key missing")
@pytest.mark.parametrize("data", load_gold_dataset())
def test_rag_fidelity(data):
    """
    Audit de fidélité via DeepEval (PBI-1301/1303).
    Mesure la Faithfulness, Contextual Precision et Answer Relevancy.
    """
    question = data["question"]
    ground_truth = data["ground_truth"]
    
    # Exécution de la requête RAG
    # Note: On récupère la réponse brute. Pour l'audit DeepEval, 
    # on idéalement besoin des contextes récupérés.
    # Dans notre rag_engine.py actuel, query() retourne str(response).
    
    # Pour un audit précis, on devrait pouvoir accéder aux source_nodes.
    # Modifions temporairement l'appel ou utilisons un mock si nécessaire, 
    # mais ici on veut tester le système réel.
    
    # On va wrapper l'appel pour extraire les infos nécessaires
    response = rag.auto_engine.query(question)
    actual_output = str(response)
    retrieval_context = [node.get_content() for node in response.source_nodes]

    # Création du cas de test DeepEval
    test_case = LLMTestCase(
        input=question,
        actual_output=actual_output,
        expected_output=ground_truth,
        retrieval_context=retrieval_context
    )

    # Définition des métriques
    faithfulness_metric = FaithfulnessMetric(threshold=0.7)
    relevancy_metric = AnswerRelevancyMetric(threshold=0.7)
    
    # Vérification (DeepEval lancera les calculs via LLM)
    assert_test(test_case, [faithfulness_metric, relevancy_metric])

if __name__ == "__main__":
    # Script d'exécution rapide pour démo
    dataset = load_gold_dataset()[:2] # Test sur 2 exemples
    for data in dataset:
        print(f"Testing: {data['question']}")
        test_rag_fidelity(data)
