import pytest
from fastapi.testclient import TestClient
from src.api import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_webhook_text_message():
    payload = {
        "event": "messages.upsert",
        "instance": "jumia",
        "data": {
            "key": {
                "remoteJid": "123456789@s.whatsapp.net",
                "fromMe": False,
                "id": "ABC123"
            },
            "message": {
                "conversation": "Bghit laptop"
            },
            "messageType": "conversation"
        }
    }
    
    with patch("src.api.chat_manager.handle_message") as mock_handle:
        mock_handle.return_value = "Hahwa laptop mzyan"
        
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 201
            
            response = client.post("/webhook", json=payload)
            
            assert response.status_code == 200
            assert response.json() == {"status": "success"}
            
            mock_handle.assert_called_once_with("123456789@s.whatsapp.net", "Bghit laptop")
            mock_post.assert_called()
            # Verify that it tried to send a message back
            args, kwargs = mock_post.call_args
            assert "message/sendText/jumia" in args[0]
            assert kwargs["json"]["number"] == "123456789@s.whatsapp.net"
            assert kwargs["json"]["text"] == "Hahwa laptop mzyan"
