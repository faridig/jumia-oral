import time
import os
import json
import logging
import re
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.llms import ChatMessage, MessageRole
from src.rag_engine import MultiQueryAutoRAG

logger = logging.getLogger(__name__)

class JumiaChatManager:
    def __init__(self, storage_path="data/sessions.json", rag_engine=None):
        self.storage_path = storage_path
        self.metadata_path = storage_path.replace(".json", "_metadata.json")
        self.chat_store = self._load_store()
        self.sessions_metadata = self._load_metadata()
        self.rag_engine = rag_engine or MultiQueryAutoRAG()
        self.ttl_seconds = 30 * 60 # 30 minutes (PBI-1801)
        
    def _load_store(self):
        if os.path.exists(self.storage_path):
            try:
                return SimpleChatStore.from_persist_path(self.storage_path)
            except Exception as e:
                logger.error(f"Erreur lors du chargement du store: {e}")
                return SimpleChatStore()
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
        last_activity = self.sessions_metadata.get(user_id, {}).get("last_activity", 0)
        
        if last_activity > 0 and (now - last_activity) > self.ttl_seconds:
            logger.info(f"Session expirée pour {user_id}. Reset de l'historique.")
            self.chat_store.delete_messages(user_id)
            if user_id in self.sessions_metadata:
                del self.sessions_metadata[user_id]
            return True
        return False

    def _parse_multimodal_response(self, text: str) -> dict:
        """
        Extrait les flux WhatsApp et TTS du texte brut du LLM (PBI-1701.3).
        """
        whatsapp_match = re.search(r'\[WHATSAPP\](.*?)\[/WHATSAPP\]', text, re.DOTALL)
        tts_match = re.search(r'\[TTS\](.*?)\[/TTS\]', text, re.DOTALL)
        
        text_whatsapp = whatsapp_match.group(1).strip() if whatsapp_match else text
        text_tts = tts_match.group(1).strip() if tts_match else text_whatsapp
        
        # Nettoyage si les balises sont absentes (fallback)
        if not whatsapp_match and not tts_match:
             # Si pas de balises, on nettoie au moins les emojis pour le TTS
             text_tts = re.sub(r'[^\w\s\.,!?]', '', text_whatsapp)
        
        return {
            "text_whatsapp": text_whatsapp,
            "text_tts": text_tts
        }

    def handle_message(self, user_id, message_text):
        # [PBI-1801] Session TTL & Mémoire
        self._check_session_expiry(user_id)
        chat_history = self.chat_store.get_messages(user_id)
        
        # [PBI-1006] Retrieval via RAG Engine
        nodes = self.rag_engine.get_retrieved_nodes(message_text)
        
        if not nodes:
             # Fallback si rien du tout
             return {"text": "Sm7 lya khouya, ma-lguit-ch chi bi si mnasib had l-wakt.", "audio_content": None, "media_url": None}

        # [PR #30] Synthesis Multimodale Native GPT-4o Audio Preview
        from src.voice import generate_multimodal_response
        multimodal_response = generate_multimodal_response(message_text, nodes, chat_history)
        
        if not multimodal_response:
             # Fallback si GPT-4o Audio échoue
             return {"text": "Sm7 lya, kayn chi mochkil f synthesis. Te9der t-3awed t-siftou?", "audio_content": None, "media_url": None}

        response_text = multimodal_response.get("text", "")
        audio_content = multimodal_response.get("audio_content")

        # Mise à jour du Store
        self.chat_store.add_message(user_id, ChatMessage(role=MessageRole.USER, content=message_text))
        self.chat_store.add_message(user_id, ChatMessage(role=MessageRole.ASSISTANT, content=response_text))
        
        # Update metadata & persist
        self.sessions_metadata[user_id] = {"last_activity": time.time()}
        self._save_store()
        
        # Extraction de l'image (Sniper Strategy)
        media_url = None
        for node_with_score in nodes:
            metadata = node_with_score.node.metadata
            if metadata.get("images"):
                images = metadata.get("images")
                if isinstance(images, list) and len(images) > 0:
                    media_url = images[0]
                    break
                elif isinstance(images, str):
                    media_url = images
                    break
        
        return {
            "text": response_text,
            "audio_content": audio_content,
            "media_url": media_url
        }

