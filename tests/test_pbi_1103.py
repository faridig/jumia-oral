import pytest
import os
from unittest.mock import MagicMock, patch
from src.voice import transcribe_audio

def test_transcribe_audio_mock():
    """
    Test basic transcription logic with mocked OpenAI and mocked open().
    """
    from unittest.mock import mock_open
    with patch("src.voice.OpenAI") as mock_openai, \
         patch("builtins.open", mock_open(read_data=b"dummy_audio_data")):
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        # Mocking transcript return value
        mock_client.audio.transcriptions.create.return_value = "Salam, bghit pc madi."
        
        # Test file path (fake)
        result = transcribe_audio("fake_path.ogg")
        
        assert result == "Salam, bghit pc madi."
        mock_client.audio.transcriptions.create.assert_called_once()
        # Verify prompt contains Darija terms
        args, kwargs = mock_client.audio.transcriptions.create.call_args
        assert "prompt" in kwargs
        assert "Darija" in kwargs["prompt"]
        assert "madi" in kwargs["prompt"]

@pytest.mark.asyncio
async def test_api_audio_webhook_handling():
    """
    Test webhook handles audioMessage by calling process_audio_and_respond via background_tasks.
    """
    from fastapi import BackgroundTasks
    from src.api import webhook
    from unittest.mock import AsyncMock
    
    mock_request = MagicMock()
    mock_request.json = AsyncMock(return_value={
        "event": "messages.upsert",
        "data": {
            "key": {
                "remoteJid": "123456@s.whatsapp.net",
                "fromMe": False,
                "id": "MSG123"
            },
            "message": {
                "audioMessage": {
                    "url": "http://example.com/audio.ogg",
                    "mimetype": "audio/ogg"
                }
            }
        }
    })
    mock_request.headers = {"apikey": "apikey"}
    
    mock_background_tasks = MagicMock(spec=BackgroundTasks)
    
    with patch("src.api.EVOLUTION_API_KEY", "apikey"):
        await webhook(mock_request, mock_background_tasks)
    
    # Check if process_audio_and_respond was added to background tasks
    mock_background_tasks.add_task.assert_called_once()
    args, kwargs = mock_background_tasks.add_task.call_args
    # First arg is the function, second is remoteJid, third is audioMessage dict
    from src.api import process_audio_and_respond
    assert args[0] == process_audio_and_respond
    assert args[1] == "123456@s.whatsapp.net"
    assert "url" in args[2]

def test_process_audio_and_respond_logic():
    """
    Test the internal logic of audio processing: download -> transcribe -> respond.
    """
    from src.api import process_audio_and_respond
    
    with patch("src.api.download_media") as mock_download, \
         patch("src.api.transcribe_audio") as mock_transcribe, \
         patch("src.api.process_and_respond") as mock_process, \
         patch("src.api.os.unlink") as mock_unlink, \
         patch("src.api.os.path.exists", return_value=True):
        
        mock_download.return_value = b"audio_data"
        mock_transcribe.return_value = "Bghit laptop mkhyr"
        
        process_audio_and_respond("123456", {"url": "http://test.com/audio.ogg"})
        
        mock_download.assert_called_once()
        mock_transcribe.assert_called_once()
        mock_process.assert_called_once_with("123456", "Bghit laptop mkhyr")
        mock_unlink.assert_called_once()
