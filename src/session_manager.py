import os
import json
import logging
from llama_index.core.storage.chat_store import SimpleChatStore
from src.rag_engine import MultiQueryAutoRAG

logger = logging.getLogger(__name__)

class JumiaChatManager:
    def __init__(self, storage_path="data/sessions.json"):
        self.storage_path = storage_path
        self.chat_store = self._load_store()
        self.rag_engine = MultiQueryAutoRAG()
        
    def _load_store(self):
        if os.path.exists(self.storage_path):
            try:
                return SimpleChatStore.from_persist_path(self.storage_path)
            except Exception as e:
                logger.error(f"Erreur lors du chargement du store: {e}")
                return SimpleChatStore()
        return SimpleChatStore()

    def _save_store(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.chat_store.persist(self.storage_path)

    def get_location(self, user_id):
        # On utilise le store pour stocker des métadonnées par utilisateur
        # Note: SimpleChatStore de LlamaIndex est normalement pour l'historique des messages.
        # On peut détourner une clé spécifique ou utiliser un dictionnaire séparé.
        # Pour rester simple et conforme au PBI, on va stocker la localisation dans les métadonnées de la session si possible,
        # ou utiliser un fichier séparé pour les profils.
        
        # Comme SimpleChatStore ne gère pas nativement les profils utilisateurs par défaut,
        # je vais implémenter une gestion hybride ou utiliser les 'chat_store' keys.
        
        # On va stocker les infos de profil dans une clé spéciale prefixée
        profile_key = f"profile_{user_id}"
        messages = self.chat_store.get_messages(profile_key)
        if messages:
            content = messages[0].content
            if isinstance(content, str):
                try:
                    profile_data = json.loads(content)
                    return profile_data.get("location")
                except Exception:
                    return None
        return None

    def set_location(self, user_id, location):
        profile_key = f"profile_{user_id}"
        from llama_index.core.llms import ChatMessage, MessageRole
        profile_data = {"location": location}
        message = ChatMessage(role=MessageRole.SYSTEM, content=json.dumps(profile_data))
        self.chat_store.set_messages(profile_key, [message])
        self._save_store()

    def handle_message(self, user_id, message_text):
        location = self.get_location(user_id)
        
        if not location:
            # Onboarding : si on ne connaît pas la ville, on vérifie si le message en contient une
            cities = ["Casablanca", "Marrakech", "Rabat", "Tanger", "Agadir", "Fès"]
            found_city = next((city for city in cities if city.lower() in message_text.lower()), None)
            
            if found_city:
                self.set_location(user_id, found_city)
                return f"Mzyan! Besseha, gha n-9teyed 3ndi bli rak f {found_city}. Kifach n9der n3awnk f Jumia l-youm?"
            else:
                return "Mrehba bik f Jumia Oral! Bach n3awnk l-max, goul lya ina mdina nti/nta fiha daba? (Ex: Ana f Casablanca)"
        
        # Si la localisation est connue, on passe au RAG
        response = self.rag_engine.query(message_text)
        
        # Extraction de l'image du premier produit si disponible
        media_url = None
        
        # On vérifie si response est un objet Response de LlamaIndex
        if hasattr(response, 'source_nodes') and response.source_nodes:
            # On cherche le premier node qui n'est pas un insight d'expert et qui a une image
            for node_with_score in response.source_nodes:
                metadata = node_with_score.node.metadata
                if not metadata.get("is_expert_insight") and metadata.get("images"):
                    images = metadata.get("images")
                    if isinstance(images, list) and len(images) > 0:
                        media_url = images[0]
                        break
                    elif isinstance(images, str):
                        media_url = images
                        break
        
        # On retourne le texte et le média éventuel
        return {
            "text": str(response),
            "media_url": media_url
        }

