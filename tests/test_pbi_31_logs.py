import pytest
from unittest.mock import patch, MagicMock
import os
import logging
from src.api import process_audio_and_respond

@patch("src.api.download_media")
@patch("src.api.transcribe_audio")
@patch("src.api.process_and_respond")
@patch("src.api.send_whatsapp_message")
def test_process_audio_and_respond_logs_transcription(mock_send, mock_process, mock_transcribe, mock_download, caplog):
    # GIVEN
    user_id = "12345"
    audio_msg = {"url": "http://fake-url.ogg"}
    mock_download.return_value = b"fake_audio_data"
    mock_transcribe.return_value = "Salam Jumia"
    
    with caplog.at_level(logging.INFO):
        # WHEN
        process_audio_and_respond(user_id, audio_msg)
        
        # THEN
        assert "🎤 Transcription audio réussie pour 12345: 'Salam Jumia'" in caplog.text
        mock_transcribe.assert_called_once()
        mock_process.assert_called_once_with(user_id, "Salam Jumia")
