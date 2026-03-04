import pytest
import os
import json
import unittest.mock
from src.session_manager import JumiaChatManager

@pytest.fixture
def chat_manager(tmp_path):
    storage_file = tmp_path / "sessions.json"
    mock_rag = unittest.mock.Mock()
    return JumiaChatManager(storage_path=str(storage_file), rag_engine=mock_rag)

def test_onboarding_flow(chat_manager):
    user_id = "user_123"
    
    # 1. Premier message : l'assistant doit demander la ville
    response = chat_manager.handle_message(user_id, "Salam!")
    assert any(word in response.lower() for word in ["ville", "fayn tina", "m9im", "mdina"])
    
    # 2. L'utilisateur donne sa ville
    response = chat_manager.handle_message(user_id, "Ana f Casablanca")
    assert "Casablanca" in chat_manager.get_location(user_id)
    assert "Mzyan" in response or "Besseha" in response
    
    # 3. Deuxième session : l'assistant se souvient de la ville
    assert chat_manager.get_location(user_id) == "Casablanca"

def test_persistence(tmp_path):
    storage_file = tmp_path / "sessions_persist.json"
    user_id = "user_456"
    mock_rag = unittest.mock.Mock()
    
    manager1 = JumiaChatManager(storage_path=str(storage_file), rag_engine=mock_rag)
    manager1.handle_message(user_id, "Salam")
    manager1.handle_message(user_id, "Marrakech")
    
    # Créer un nouveau manager pointant sur le même fichier
    manager2 = JumiaChatManager(storage_path=str(storage_file), rag_engine=mock_rag)
    assert manager2.get_location(user_id) == "Marrakech"
