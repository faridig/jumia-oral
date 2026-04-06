import unittest.mock as mock
from src.api import process_and_respond

@mock.patch("src.api.send_whatsapp_message")
@mock.patch("src.api.send_whatsapp_audio")
@mock.patch("src.api.get_chat_manager")
def test_reproduction_empty_text(mock_get_chat_manager, mock_send_audio, mock_send_text):
    # Mock chat manager returning None for text
    mock_chat_manager = mock.MagicMock()
    mock_get_chat_manager.return_value = mock_chat_manager
    mock_chat_manager.handle_message.return_value = {
        "text": None,
        "audio_content": b"fake_audio",
        "media_url": None
    }
    
    # Run
    process_and_respond("12345", "test")
    
    # Check what was sent to send_whatsapp_message
    mock_send_text.assert_called_with("12345", None)

if __name__ == "__main__":
    try:
        test_reproduction_empty_text()
        print("Test passed (logic-wise), now we know None is passed to send_whatsapp_message")
    except Exception as e:
        print(f"Test failed: {e}")
