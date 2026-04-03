import unittest.mock as mock
from src.api import process_and_respond

@mock.patch("src.api.send_whatsapp_message")
@mock.patch("src.api.send_whatsapp_audio")
@mock.patch("src.api.generate_speech")
@mock.patch("src.api.get_chat_manager")
def test_pbi_2001_sequencing(mock_get_chat_manager, mock_generate_speech, mock_send_audio, mock_send_text):
    # Mock chat manager response
    mock_chat_manager = mock.MagicMock()
    mock_get_chat_manager.return_value = mock_chat_manager
    mock_chat_manager.handle_message.return_value = {
        "text": "Texte WhatsApp",
        "text_tts": "Texte TTS",
        "media_url": "http://image.url"
    }
    
    # Mock generate_speech
    mock_generate_speech.return_value = b"audio_content"
    
    calls = []
    def record_call(name):
        def wrapper(*args, **kwargs):
            calls.append(name)
        return wrapper
    
    mock_send_audio.side_effect = record_call('audio')
    mock_send_text.side_effect = record_call('text')

    # Run the function
    process_and_respond("user123", "Bghit PC")
    
    print(f"Calls order: {calls}")
    
    # Target order for Sprint 20: Audio first, then Text/Link
    assert 'audio' in calls, "Audio should be sent"
    assert 'text' in calls, "Text should be sent"
    
    # For Sprint 20, audio should be sent before the first text message
    assert calls.index('audio') < calls.index('text'), "Audio must be sent BEFORE text/link"

