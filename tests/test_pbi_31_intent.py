import pytest
from unittest.mock import patch, MagicMock
from src.session_manager import JumiaChatManager
from src.voice import generate_multimodal_response

def test_intent_detection_skips_rag_on_greeting():
    # GIVEN
    manager = JumiaChatManager()
    user_query = "Salam jumia"
    
    with patch("src.rag_engine.llm") as mock_llm_obj:
        mock_llm_obj.complete.return_value.text = "GREETING"
        
        # WHEN
        intent = manager.rag_engine.detect_intent(user_query)
        nodes = manager.rag_engine.get_retrieved_nodes(user_query, intent=intent)
        
        # THEN
        assert intent == "GREETING"
        assert nodes == []

def test_multimodal_no_forced_link_on_greeting():
    # GIVEN
    user_query = "Salam"
    context_nodes = [MagicMock()] # Some nodes found but intent is greeting
    intent = "GREETING"
    
    with patch("openai.resources.chat.completions.Completions.create") as mock_openai:
        mock_resp = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "" # Lazy model
        mock_message.audio.data = b"ZmFrZV9hdWRpbw=="
        mock_message.audio.transcript = "Mrehba bik!"
        mock_choice.message = mock_message
        mock_resp.choices = [mock_choice]
        mock_openai.return_value = mock_resp
        
        # WHEN
        resp = generate_multimodal_response(user_query, context_nodes, intent=intent)
        
        # THEN
        assert "Khoudou mn hna" not in resp["text"]
        assert resp["text"] == "Mrehba bik!"

def test_multimodal_forced_link_on_product_intent():
    # GIVEN
    user_query = "Bghit laptop"
    mock_node = MagicMock()
    mock_node.node.metadata = {"name": "Thinkpad", "price_numeric": 5000, "url": "http://link"}
    context_nodes = [mock_node]
    intent = "PRODUCT"
    
    with patch("openai.resources.chat.completions.Completions.create") as mock_openai:
        mock_resp = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "" # Lazy model
        mock_message.audio.data = b"ZmFrZV9hdWRpbw=="
        mock_message.audio.transcript = "Ha wahed laptop naddi."
        mock_choice.message = mock_message
        mock_resp.choices = [mock_choice]
        mock_openai.return_value = mock_resp
        
        # WHEN
        resp = generate_multimodal_response(user_query, context_nodes, intent=intent)
        
        # THEN
        assert "Thinkpad" in resp["text"]
        assert "http://link" in resp["text"]
