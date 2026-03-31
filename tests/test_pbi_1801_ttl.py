import os
import time
import pytest
from unittest.mock import MagicMock, patch
from src.session_manager import JumiaChatManager
from llama_index.core.llms import ChatMessage, MessageRole

@pytest.fixture
def chat_manager():
    storage_path = "data/test_sessions_ttl.json"
    metadata_path = storage_path.replace(".json", "_metadata.json")
    if os.path.exists(storage_path):
        os.remove(storage_path)
    if os.path.exists(metadata_path):
        os.remove(metadata_path)
    
    with patch("src.session_manager.MultiQueryAutoRAG") as mock_rag_class:
        mock_rag = MagicMock()
        mock_rag.query.return_value = "[WHATSAPP]Mrehba! Hahwa laptop.[/WHATSAPP][TTS]Mrehba[/TTS]"
        mock_rag_class.return_value = mock_rag
        
        manager = JumiaChatManager(storage_path=storage_path)
        yield manager
    
    if os.path.exists(storage_path):
        os.remove(storage_path)
    if os.path.exists(metadata_path):
        os.remove(metadata_path)

def test_pbi_1801_session_ttl_expiry(chat_manager):
    user_id = "test_user_ttl"
    
    # 1. On injecte manuellement un message et une activité datant de 31 min
    chat_manager.chat_store.add_message(user_id, ChatMessage(role=MessageRole.USER, content="Hello Old Message"))
    chat_manager.sessions_metadata[user_id] = {"last_activity": time.time() - (31 * 60)}
    chat_manager._save_store()
    
    # Vérification que l'ancien message est bien là avant le test
    assert len(chat_manager.chat_store.get_messages(user_id)) == 1
    
    # 2. L'utilisateur envoie un nouveau message
    chat_manager.handle_message(user_id, "Bghit chi bi si jdid")
    
    # 3. L'historique précédent doit être vide (Scenario 1)
    messages = chat_manager.chat_store.get_messages(user_id)
    contents = [m.content for m in messages]
    
    assert "Hello Old Message" not in contents
    # On doit avoir le nouveau message USER + la réponse ASSISTANT = 2 messages
    assert len(messages) == 2
    assert "Bghit chi bi si jdid" in contents

def test_pbi_1801_persona_maintenance(chat_manager):
    user_id = "test_user_persona"
    
    # GIVEN un reset de session (session vide par défaut ou expirée)
    # WHEN le bot répond
    response = chat_manager.handle_message(user_id, "Salam")
    
    # THEN Il conserve son ton Darija (Mrehba) et ses instructions (Scenario 2)
    assert "Mrehba" in response["text"] or "Salam" in response["text"]
    # On vérifie qu'on a bien les balises multimédia gérées (le texte est propre)
    assert "[WHATSAPP]" not in response["text"]
    assert "text_tts" in response
