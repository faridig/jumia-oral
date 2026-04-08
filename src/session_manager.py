import time
import os
import json
import logging
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.llms import ChatMessage, MessageRole
from src.rag_engine import MultiQueryAutoRAG
from src.voice import generate_multimodal_response

logger = logging.getLogger(__name__)


class JumiaChatManager:
    def __init__(self, storage_path="data/sessions.json", rag_engine=None):
        self.storage_path = storage_path
        self.metadata_path = storage_path.replace(".json", "_metadata.json")
        self.chat_store = self._load_store()
        self.sessions_metadata = self._load_metadata()
        self.rag_engine = rag_engine or MultiQueryAutoRAG()
        self.ttl_seconds = 30 * 60

    def _load_store(self):
        if os.path.exists(self.storage_path):
            try:
                return SimpleChatStore.from_persist_path(self.storage_path)
            except Exception as e:
                logger.error(f"Erreur chargement store: {e}")
        return SimpleChatStore()

    def _load_metadata(self):
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_store(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.chat_store.persist(self.storage_path)
        self._save_metadata()

    def _save_metadata(self):
        try:
            with open(self.metadata_path, 'w') as f:
                json.dump(self.sessions_metadata, f)
        except Exception as e:
            logger.error(f"Erreur sauvegarde métadonnées: {e}")

    def _check_session_expiry(self, user_id):
        now = time.time()
        last_activity = self.sessions_metadata.get(
            user_id, {}
        ).get("last_activity", 0)

        if last_activity > 0 and (now - last_activity) > self.ttl_seconds:
            self.chat_store.delete_messages(user_id)
            if user_id in self.sessions_metadata:
                del self.sessions_metadata[user_id]
            return True
        return False

    def handle_message(self, user_id, message_text):
        self._check_session_expiry(user_id)
        chat_history = self.chat_store.get_messages(user_id)

        # 1. Détection d'intention (PBI-31 Fix)
        intent = self.rag_engine.detect_intent(message_text)

        # 2. RAG conditionnel
        nodes = []
        if "PRODUCT" in intent:
            nodes = self.rag_engine.get_retrieved_nodes(message_text, intent=intent)
            if not nodes:
                logger.warning("Intention produit mais aucun résultat RAG.")
                return {"text": "Sm7 lya khouya, ma-lguit-ch chi laptop b had l-mouwasafat.", "audio_content": None}
        else:
            logger.info(f"Pas de recherche produit pour l'intention: {intent}")

        # 3. Génération réponse
        multi_resp = generate_multimodal_response(
            message_text, nodes, chat_history, intent=intent
        )

        if not multi_resp:
            return {"text": "Mochkil f synthesis.", "audio_content": None}

        resp_text = multi_resp.get("text", "")
        audio_content = multi_resp.get("audio_content")

        self.chat_store.add_message(
            user_id,
            ChatMessage(role=MessageRole.USER, content=message_text)
        )
        self.chat_store.add_message(
            user_id,
            ChatMessage(role=MessageRole.ASSISTANT, content=resp_text)
        )

        self.sessions_metadata[user_id] = {"last_activity": time.time()}
        self._save_store()

        media_url = None
        for n in nodes:
            images = n.node.metadata.get("images")
            if images:
                media_url = images[0] if isinstance(images, list) else images
                break

        return {
            "text": resp_text,
            "audio_content": audio_content,
            "media_url": media_url
        }
