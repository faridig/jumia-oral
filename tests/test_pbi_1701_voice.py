import pytest
from src.voice import generate_speech
import os
import base64
from unittest.mock import patch, MagicMock

@patch("src.voice.OpenAI")
def test_generate_speech_native_audio_success(mock_openai):
    """
    Test de la migration vers OpenAI Native Audio (gpt-4o-audio-preview).
    PBI-1701.1 UPGRADE (PR #24).
    """
    # Configuration du mock
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    # Mocking de la réponse Chat Completion Audio
    mock_choice = MagicMock()
    mock_choice.message.audio.data = base64.b64encode(b"fake_audio_onyx_opus").decode('utf-8')
    mock_client.chat.completions.create.return_value.choices = [mock_choice]
    
    text_darija = "Khouya, had l-bi si naddi bzaf, madi!"
    
    # Appel à la fonction (onyx par défaut)
    audio_content = generate_speech(text_darija)
    
    assert audio_content is not None
    assert audio_content == b"fake_audio_onyx_opus"
    
    # Vérifie les paramètres d'appel
    mock_client.chat.completions.create.assert_called_with(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "onyx", "format": "opus"},
        messages=[
            {"role": "system", "content": "Tu es un vendeur expert en informatique à Casablanca. PARLE EXCLUSIVEMENT EN DARIJA MAROCAIN (DARIJA T-MAGHRIBIYA). INTERDICTION totale d'utiliser le français ou l'arabe classique. Utilise un vocabulaire de proximité (khouya, sahbi, l-m3aqoul, tayra, madi, l-hemza). Ton débit doit être rapide, sec et direct. Prononce les 'J' de manière douce (Maroc) et non comme des 'G' (Égypte)."},
            {"role": "user", "content": text_darija}
        ]
    )
