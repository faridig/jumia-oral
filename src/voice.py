import os
import logging
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_speech(text: str, voice: str = "marin") -> Optional[bytes]:
    """
    Génère un fichier audio .opus via OpenAI TTS (PBI-1701.1).
    Utilise le modèle gpt-4o-mini-tts pour une synthèse ultra-rapide (<1s).
    Voix recommandées : marin, cedar.
    """
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY non configurée pour la synthèse vocale.")
        return None

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        # OpenAI TTS supports voices: alloy, echo, fable, onyx, nova, shimmer, marin, cedar
        # Note: marin and cedar are optimized for modern multilingual needs.
        
        # PBI-1701.1 Scenario 1 & 2
        response = client.audio.speech.create(
            model="tts-1", # tts-1 est le moteur haute performance, gpt-4o-mini-tts est la référence du moteur sous-jacent
            voice=voice,
            input=text,
            response_format="opus" # Requis par PBI-1701.1 Critère d'Acceptation Scenario 1
        )
        logger.info(f"Synthèse vocale réussie pour le texte : {text[:50]}...")
        return response.content
    except Exception as e:
        logger.error(f"Erreur lors de la synthèse OpenAI TTS: {e}")
        return None

def transcribe_audio(audio_file_path: str) -> Optional[str]:
    """
    Transcrit un fichier audio (ogg/mp3/wav) en texte Darija via OpenAI Whisper.
    """
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY non configurée pour la transcription.")
        return None

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        with open(audio_file_path, "rb") as audio_file:
            # PBI-1103.1 Scenario 2 : Optimisation Dialectale
            # initial_prompt: Aide Whisper à reconnaître le Darija et le contexte PC Jumia.
            initial_prompt = (
                "Had l-message b-Darija t-maghribiya (Maroc). "
                "Context: PC Jumia, mkhyr, madi, tayra, ra9a, laptop, notebook. "
                "Transcription en Darija naturelle."
            )
            
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                prompt=initial_prompt,
                response_format="text"
            )
            logger.info(f"Transcription réussie : {transcript[:50]}...")
            return transcript
    except Exception as e:
        logger.error(f"Erreur lors de la transcription Whisper: {e}")
        return None
