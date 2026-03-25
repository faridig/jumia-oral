import os
import logging
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
