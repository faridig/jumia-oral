import unittest.mock as mock
from src.api import process_and_respond

@mock.patch("src.api.send_whatsapp_message")
@mock.patch("src.api.send_whatsapp_audio")
@mock.patch("src.api.get_chat_manager")
def test_pbi_2001_sequencing(mock_get_chat_manager, mock_send_audio, mock_send_text):
    # Mock chat manager response to match multimodal native structure
    mock_chat_manager = mock.MagicMock()
    mock_get_chat_manager.return_value = mock_chat_manager
    mock_chat_manager.handle_message.return_value = {
        "text": "Texte WhatsApp",
        "audio_content": b"audio_content",
        "media_url": "http://image.url"
    }
    
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
    # In process_and_respond: 
    # 1. send_whatsapp_audio (for audio_content) -> 'audio'
    # 2. send_whatsapp_message (for media_url) -> 'text'
    # 3. send_whatsapp_message (for text) -> 'text'
    
    assert calls[0] == 'audio', "Audio must be sent FIRST"
    assert 'text' in calls[1:], "Text must be sent AFTER audio"

