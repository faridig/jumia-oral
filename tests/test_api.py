import pytest
from fastapi.testclient import TestClient
from src.api import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_webhook_text_message():
    payload = {
        "event": "messages.upsert",
        "instance": "Jumia-Oral-Agent",
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
    
    headers = {"apikey": "apikey"}
    
    with patch("src.api.get_chat_manager") as mock_get_chat:
        mock_chat = MagicMock()
        mock_chat.handle_message.return_value = "Hahwa laptop mzyan"
        mock_get_chat.return_value = mock_chat
        
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 201
            
            # PBI-803 : On ajoute l'apikey dans les headers du test
            response = client.post("/webhook", json=payload, headers=headers)
            
            assert response.status_code == 200
            assert response.json() == {"status": "success"}
            
            mock_chat.handle_message.assert_called_once_with("123456789@s.whatsapp.net", "Bghit laptop")
            mock_post.assert_called()
            # Verify that it tried to send a message back
            args, kwargs = mock_post.call_args
            # Vérification de la nouvelle instance (PBI-801)
            assert "message/sendText/Jumia-Oral-Agent" in args[0]
            # Vérification du numéro sans le suffixe (PBI-803)
            assert kwargs["json"]["number"] == "123456789"
            assert kwargs["json"]["text"] == "Hahwa laptop mzyan"
