import pytest
from unittest.mock import MagicMock, patch, ANY
from src.session_manager import JumiaChatManager

@patch("src.session_manager.MultiQueryAutoRAG")
@patch("src.session_manager.SimpleChatStore")
def test_handle_message_no_location_onboarding(mock_chat_store, mock_rag_engine):
    """
    PBI-1006: Ensure that we no longer ask for location.
    """
    mock_rag = MagicMock()
    mock_rag.query.return_value = "Hahwa laptop mzyan"
    mock_rag_engine.return_value = mock_rag
    
    manager = JumiaChatManager(storage_path="data/test_sessions.json")
    
    # We should directly get the RAG response without asking for location
    response = manager.handle_message("user123", "Bghit laptop")
    
    # The response should be from the RAG (as a dict because of how handle_message works)
    assert response["text"] == "Hahwa laptop mzyan"
    mock_rag.query.assert_called_once_with("Bghit laptop", chat_history=ANY)
