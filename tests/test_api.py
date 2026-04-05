import pytest
from fastapi.testclient import TestClient
from src.api import app
from unittest.mock import patch, MagicMock

client = TestClient(app)


@patch("src.api.get_chat_manager")
def test_webhook_text_message(mock_get_chat):
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

    mock_chat = MagicMock()
    mock_chat.handle_message.return_value = {
        "text": "*HP Laptop* - 5000 MAD",
        "audio_content": b"fake_audio_content",
        "media_url": "http://image.jpg"
    }
    mock_get_chat.return_value = mock_chat

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 201

        response = client.post("/webhook", json=payload, headers=headers)

        assert response.status_code == 200
        assert response.json() == {"status": "success"}

        mock_chat.handle_message.assert_called_once()
        assert mock_post.call_count == 3


def test_send_whatsapp_audio_v2_payload():
    from src.api import send_whatsapp_audio
    import base64

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 201

        number = "212600000000@s.whatsapp.net"
        audio_content = b"fake_audio_binary"
        audio_base64 = base64.b64encode(audio_content).decode('utf-8')

        send_whatsapp_audio(number, audio_content)

        assert mock_post.called
        args, kwargs = mock_post.call_args
        payload = kwargs["json"]

        assert "message/sendWhatsAppAudio/Jumia-Oral-Agent" in args[0]
        assert payload["number"] == "212600000000"
        assert payload["audio"] == audio_base64
        assert payload["ptt"] is True
