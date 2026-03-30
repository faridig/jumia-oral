import pytest
from src.voice import generate_speech
import os
from unittest.mock import patch, MagicMock

@patch("src.voice.OpenAI")
def test_generate_speech_success(mock_openai):
    """
    Scenario 1 : Utilisation du modèle gpt-4o-mini-tts (PBI-1701.1)
    Scenario 2 : Optimisation de la voix (PBI-1701.1) - Correction Post-Audit (nova)
    """
    # Configuration du mock
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.audio.speech.create.return_value.content = b"fake_audio_opus_content"
    
    text_darija = "Had l-PC madi bzaaf, mkhyr l-khidma."
    
    # Appel à la fonction à implémenter (nova est recommandée pour le Darija)
    audio_content = generate_speech(text_darija, voice="nova")
    
    assert audio_content is not None
    assert len(audio_content) > 0
    # Vérifie que c'est bien du binaire
    assert isinstance(audio_content, bytes)
    assert audio_content == b"fake_audio_opus_content"
    
    # Vérifie les paramètres d'appel
    mock_client.audio.speech.create.assert_called_with(
        model="tts-1",
        voice="nova",
        input=text_darija,
        response_format="opus"
    )

@patch("src.voice.OpenAI")
def test_generate_speech_with_shimmer(mock_openai):
    """
    Scenario 2 : Optimisation de la voix (PBI-1701.1) - Correction Post-Audit (shimmer)
    """
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.audio.speech.create.return_value.content = b"fake_audio_shimmer"
    
    text_darija = "Mrehba bikom f Jumia, bghit chi PC?"
    audio_content = generate_speech(text_darija, voice="shimmer")
    
    assert audio_content is not None
    assert len(audio_content) > 0
    assert isinstance(audio_content, bytes)
    assert audio_content == b"fake_audio_shimmer"
    
    mock_client.audio.speech.create.assert_called_with(
        model="tts-1",
        voice="shimmer",
        input=text_darija,
        response_format="opus"
    )
