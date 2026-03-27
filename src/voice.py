import os
import logging
import base64
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_speech(text: str, voice: str = "onyx") -> Optional[bytes]:
    """
    Génère un fichier audio .opus via OpenAI Native Audio (gpt-4o-audio-preview).
    PBI-1701.1 UPGRADE : Migration vers l'audio natif pour un accent 100% Casa.
    Voix Championne : onyx (Profondeur & Grain Expert/Street).
    """
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY non configurée pour la synthèse vocale.")
        return None

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Style Prompt "Expert de Casablanca" (Migration PR #24)
        style_prompt = (
            "Tu es un vendeur expert en informatique à Casablanca. "
            "PARLE EXCLUSIVEMENT EN DARIJA MAROCAIN (DARIJA T-MAGHRIBIYA). "
            "INTERDICTION totale d'utiliser le français ou l'arabe classique. "
            "Utilise un vocabulaire de proximité (khouya, sahbi, l-m3aqoul, tayra, madi, l-hemza). "
            "Ton débit doit être rapide, sec et direct. "
            "Prononce les 'J' de manière douce (Maroc) et non comme des 'G' (Égypte)."
        )
        
        # PBI-1701.1 Golden Config : Native Audio GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": voice, "format": "opus"},
            messages=[
                {"role": "system", "content": style_prompt},
                {"role": "user", "content": text}
            ]
        )
        
        # Extraction de l'audio binaire (base64 décodé)
        audio_data_b64 = response.choices[0].message.audio.data
        audio_content = base64.b64decode(audio_data_b64)
        
        logger.info(f"Génération Native Audio (GPT-4o) réussie pour : {text[:50]}...")
        return audio_content
    except Exception as e:
        logger.error(f"Erreur lors de la génération Native Audio (GPT-4o): {e}")
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
