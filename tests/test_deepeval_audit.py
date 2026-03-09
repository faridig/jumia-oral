import os
import json
import pytest
import random
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval import assert_test
from src.rag_engine import MultiQueryAutoRAG

# Stabilisation DeepEval & Économie de Tokens (Sprint 13 Guidance)
os.environ["DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE"] = "300"
EVAL_MODEL = "gpt-4o-mini" # Low-Cost Mode pour l'évaluateur

# Initialisation du moteur RAG
rag = MultiQueryAutoRAG()

def load_gold_dataset(request):
    """
    Charge le dataset avec mode Low-Cost (Guidance 1 & 4).
    """
    if not os.getenv("OPENAI_API_KEY") and os.getenv("GITHUB_ACTIONS") == "true":
        return []
        
    try:
        with open("tests/gold_dataset.json", "r") as f:
            data = json.load(f)
            # Mode Low-Cost : 3 cas aléatoires par défaut
            if not request.config.getoption("--full-audit"):
                return random.sample(data, min(3, len(data)))
            return data
    except FileNotFoundError:
        return []

@pytest.fixture
def gold_data_sample(request):
    return load_gold_dataset(request)

def test_rag_fidelity(gold_data_sample):
    """
    Audit de fidélité via DeepEval (PBI-1301/1303).
    Utilise gpt-4o-mini comme évaluateur pour économiser les tokens.
    """
    for data in gold_data_sample:
        question = data["question"]
        ground_truth = data["ground_truth"]
        
        # Exécution de la requête RAG
        response = rag.auto_engine.query(question)
        actual_output = str(response)
        retrieval_context = [node.get_content() for node in response.source_nodes]

        # Création du cas de test
        test_case = LLMTestCase(
            input=question,
            actual_output=actual_output,
            expected_output=ground_truth,
            retrieval_context=retrieval_context
        )

        # Définition des métriques avec évaluateur économique
        faithfulness_metric = FaithfulnessMetric(threshold=0.7, model=EVAL_MODEL)
        relevancy_metric = AnswerRelevancyMetric(threshold=0.7, model=EVAL_MODEL)
        
        assert_test(test_case, [faithfulness_metric, relevancy_metric])

if __name__ == "__main__":
    # Démo rapide
    pass
