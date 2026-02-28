import os
import logging
from src.rag_engine import MultiQueryAutoRAG

# Configuration du logging pour le test
logging.basicConfig(level=logging.INFO)

def test_low_quality_warning():
    """
    Vérifie que le LLM avertit l'utilisateur pour un produit avec un trust_score de 0.
    """
    rag = MultiQueryAutoRAG()
    
    # Le produit "Jedel Haut Parleur" a un trust_score de 0.0 dans nos données.
    query = "Bghit baffes rkhisa dyal pc (Jedel)"
    response = rag.query(query)
    
    print(f"\nQUERY: {query}")
    print(f"RESPONSE: {response}")
    
    # Vérification de la présence d'un avertissement (ton local ou mot clé)
    response_text = str(response).lower()
    warning_keywords = ["attention", "risk", "vigilant", "0.0", "pas assez d'avis", "chouf"]
    has_warning = any(kw in response_text for kw in warning_keywords)
    
    if has_warning:
        print("\n✅ Test Passé : Le LLM a émis un avertissement pour le produit à faible score.")
    else:
        print("\n❌ Test Échoué : Le LLM n'a pas semblé avertir l'utilisateur.")

if __name__ == "__main__":
    test_low_quality_warning()
