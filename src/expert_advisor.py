import os
import logging
from typing import Optional
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core import PromptTemplate

load_dotenv()
logger = logging.getLogger(__name__)

# Mapping des catégories vers des Personas d'Experts (Context7 Style)
PERSONA_MAPPING = {
    "beauté & santé": "Expert Dermatologue",
    "beauté & soins": "Expert Dermatologue",
    "informatique": "Architecte Système & Tech Analyst",
    "smartphones": "Analyste Mobile",
    "matériels de jeu gamer": "Pro Gamer & Hardware Expert",
    "maison, cuisine & bureau": "Conseiller en Aménagement & Électroménager",
    "chaussures homme": "Conseiller Style & Sport",
    "vêtements homme": "Conseiller Mode",
}

class ExpertAdvisor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(model="gpt-4o-mini", api_key=self.api_key)

    def get_expert_insight(self, product_name: str, category: str) -> str:
        persona = PERSONA_MAPPING.get(category.lower(), "Expert Conseil")
        
        prompt = PromptTemplate(
            "Tu agis en tant que {persona}. "
            "Donne un conseil d'usage professionnel et un bienfait technique pour le produit suivant : {product_name}. "
            "Le conseil doit être court, percutant et en Français (pour être traduit ou adapté ensuite). "
            "CONSIGNE DE SÉCURITÉ : Ne mentionne JAMAIS de prix ou de sites concurrents. "
            "Si le produit est inconnu, donne un conseil général lié à sa catégorie ({category}).\n"
            "Conseil d'Expert :"
        )
        
        try:
            response = self.llm.complete(prompt.format(persona=persona, product_name=product_name, category=category))
            return response.text.strip()
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'insight expert: {e}")
            return "Profitez de la qualité Jumia au meilleur prix."

expert_advisor = ExpertAdvisor()
