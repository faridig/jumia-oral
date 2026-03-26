import pytest
from src.voice import generate_speech
import os
from unittest.mock import patch, MagicMock

@patch("src.voice.OpenAI")
def test_generate_speech_success(mock_openai):
    """
    Scenario 1 : Utilisation du modèle gpt-4o-mini-tts (PBI-1701.1)
    Scenario 2 : Optimisation de la voix (PBI-1701.1)
    """
    # Configuration du mock
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.audio.speech.create.return_value.content = b"fake_audio_opus_content"
    
    text_darija = "Had l-PC madi bzaaf, mkhyr l-khidma."
    
    # Appel à la fonction à implémenter
    audio_content = generate_speech(text_darija, voice="marin")
    
    assert audio_content is not None
    assert len(audio_content) > 0
    # Vérifie que c'est bien du binaire
    assert isinstance(audio_content, bytes)
    assert audio_content == b"fake_audio_opus_content"
    
    # Vérifie les paramètres d'appel
    mock_client.audio.speech.create.assert_called_with(
        model="tts-1",
        voice="marin",
        input=text_darija,
        response_format="opus"
    )

@patch("src.voice.OpenAI")
def test_generate_speech_with_cedar(mock_openai):
    """
    Scenario 2 : Optimisation de la voix (PBI-1701.1)
    """
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.audio.speech.create.return_value.content = b"fake_audio_cedar"
    
    text_darija = "Mrehba bikom f Jumia, bghit chi PC?"
    audio_content = generate_speech(text_darija, voice="cedar")
    
    assert audio_content is not None
    assert len(audio_content) > 0
    assert isinstance(audio_content, bytes)
    assert audio_content == b"fake_audio_cedar"
    
    mock_client.audio.speech.create.assert_called_with(
        model="tts-1",
        voice="cedar",
        input=text_darija,
        response_format="opus"
    )
