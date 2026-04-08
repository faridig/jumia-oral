import pytest
from unittest.mock import MagicMock, patch, ANY
from src.session_manager import JumiaChatManager

@patch("src.session_manager.generate_multimodal_response")
@patch("src.session_manager.MultiQueryAutoRAG")
@patch("src.session_manager.SimpleChatStore")
def test_handle_message_no_location_onboarding(mock_chat_store, mock_rag_engine, mock_gen_multimodal):
    """
    PBI-1006: Ensure that we no longer ask for location.
    """
    mock_rag = MagicMock()
    mock_rag.detect_intent.return_value = "PRODUCT"
    mock_rag.get_retrieved_nodes.return_value = [MagicMock()]
    mock_rag_engine.return_value = mock_rag
    
    mock_gen_multimodal.return_value = {
        "text": "Hahwa laptop mzyan",
        "audio_content": b"audio"
    }

    manager = JumiaChatManager(storage_path="data/test_sessions.json")

    # We should directly get the RAG response without asking for location
    response = manager.handle_message("user123", "Bghit laptop")

    # The response should be from the RAG
    assert response["text"] == "Hahwa laptop mzyan"
    mock_rag.get_retrieved_nodes.assert_called_once_with("Bghit laptop", intent="PRODUCT")
