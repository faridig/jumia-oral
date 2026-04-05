import os
import logging
import base64
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def generate_multimodal_response(
    user_query: str, context_nodes: list, chat_history: list = None
) -> dict:
    """
    Génère une réponse multimodale (Texte + Audio natif).
    """
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY non configurée pour GPT-4o Audio.")
        return None

    client = OpenAI(api_key=OPENAI_API_KEY)

    # 1. Préparation du contexte technique
    nodes_info = []
    for n in context_nodes:
        m = n.node.metadata
        nodes_info.append(
            f"Produit: {m.get('name')}\n"
            f"Prix: {m.get('price_numeric')} MAD\n"
            f"Specs: {m.get('description')}\n"
            f"URL: {m.get('url')}"
        )
    context_text = "\n---\n".join(nodes_info)

    # 2. Historique conversationnel
    history_text = ""
    if chat_history:
        history_text = "\n".join([f"{m.role}: {m.content}" for m in chat_history[-5:]])

    # 3. Système Prompt CASA
    system_prompt = (
        "Tu es le 'Compagnon Notebook Jumia', un vendeur expert à Casablanca.\n"
        "PROSODIE : Speak as a warm, persuasive Moroccan personal shopper. "
        "Use natural Darija intonations, emphasize 'hemza'.\n\n"
        "CONSIGNES :\n"
        "1. Choisis LE MEILLEUR produit parmi les nodes fournis.\n"
        "2. Texte: message WhatsApp minimaliste : *NOM* - *PRIX* MAD \n\n "
        "Khoudou mn hna : [URL]\n"
        "3. Audio: conseil chaleureux en Darija Casa.\n"
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": "marin", "format": "opus"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": f"CONTEXTE:\n{context_text}"},
                {"role": "system", "content": f"HISTORIQUE:\n{history_text}"},
                {"role": "user", "content": user_query}
            ]
        )

        audio_data = base64.b64decode(completion.choices[0].message.audio.data)
        text_whatsapp = completion.choices[0].message.content

        return {
            "text": text_whatsapp,
            "audio_content": audio_data
        }
    except Exception as e:
        logger.error(f"Erreur GPT-4o Audio: {e}")
        return None


def generate_speech(text: str, voice: str = "marin") -> Optional[bytes]:
    """
    Génère un fichier audio .opus via OpenAI TTS.
    """
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY non configurée.")
        return None

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            response_format="opus"
        )
        return response.content
    except Exception as e:
        logger.error(f"Erreur TTS: {e}")
        return None


def transcribe_audio(audio_file_path: str) -> Optional[str]:
    """
    Transcrit un fichier audio via OpenAI Whisper.
    """
    if not OPENAI_API_KEY:
        return None

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        with open(audio_file_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text"
            )
            return transcript
    except Exception as e:
        logger.error(f"Erreur Whisper: {e}")
        return None
