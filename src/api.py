import os
import logging
import requests
import tempfile
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from src.session_manager import JumiaChatManager
from src.voice import transcribe_audio
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Jumia Oral WhatsApp Gateway")
_chat_manager = None


def get_chat_manager():
    global _chat_manager
    if _chat_manager is None:
        _chat_manager = JumiaChatManager()
    return _chat_manager


EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://localhost:8080")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "apikey")
INSTANCE_NAME = os.getenv("INSTANCE_NAME", "Jumia-Oral-Agent")


def send_whatsapp_message(number: str, text: str, media_url: str = None):
    """Envoie un message texte ou média via Evolution API."""
    if media_url:
        url = f"{EVOLUTION_API_URL}/message/sendMedia/{INSTANCE_NAME}"
        payload = {
            "number": number.split("@")[0],
            "media": media_url,
            "caption": text,
            "mediaType": "image",
            "delay": 500
        }
    else:
        url = f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE_NAME}"
        payload = {
            "number": number.split("@")[0],
            "text": text,
            "delay": 500,
            "linkPreview": True
        }

    headers = {
        "Content-Type": "application/json",
        "apikey": EVOLUTION_API_KEY
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logger.info(f"INFO - Message envoyé à {number}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message: {e}")


def send_whatsapp_audio(number: str, audio_content: bytes):
    """Envoie un message vocal (.opus) via Evolution API."""
    import base64
    url = f"{EVOLUTION_API_URL}/message/sendWhatsAppAudio/{INSTANCE_NAME}"
    audio_base64 = base64.b64encode(audio_content).decode('utf-8')

    payload = {
        "number": number.split("@")[0],
        "audio": audio_base64,
        "ptt": True,
        "delay": 1200
    }

    headers = {
        "Content-Type": "application/json",
        "apikey": EVOLUTION_API_KEY
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logger.info(f"INFO - Audio envoyé à {number}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'audio: {e}")


def process_and_respond(user_id: str, text: str):
    logger.info(f"Début du traitement pour {user_id}")
    chat_response = get_chat_manager().handle_message(user_id, text)

    if isinstance(chat_response, dict):
        response_text = chat_response.get("text")
        audio_content = chat_response.get("audio_content")
        media_url = chat_response.get("media_url")

        # 1. Priorité à l'audio (native)
        if audio_content:
            send_whatsapp_audio(user_id, audio_content)
        
        # 2. Lien image si présent
        if media_url:
            send_whatsapp_message(user_id, "", media_url)
        
        # 3. Message texte (robustesse : check null)
        if response_text and response_text.strip():
            send_whatsapp_message(user_id, response_text)
    else:
        # Fallback pour string simple
        text_resp = str(chat_response)
        if text_resp.strip():
            send_whatsapp_message(user_id, text_resp)


def download_media(url: str):
    headers = {"apikey": EVOLUTION_API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content


def process_audio_and_respond(user_id: str, audio_msg: dict):
    url = audio_msg.get("url")
    if not url:
        return

    try:
        audio_data = download_media(url)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
            tmp.write(audio_data)
            tmp_path = tmp.name

        text = transcribe_audio(tmp_path)
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

        if text:
            process_and_respond(user_id, text)
        else:
            send_whatsapp_message(user_id, "Sm7 lya, ma-9dertch n-sm3.")
    except Exception as e:
        logger.error(f"Erreur traitement audio: {e}")


@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    provided_key = request.headers.get("apikey")
    if provided_key != EVOLUTION_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()
    if data.get("event") == "messages.upsert":
        msg_data = data.get("data", {})
        key = msg_data.get("key", {})
        if key.get("fromMe", False):
            return {"status": "ignored"}

        remote_jid = key.get("remoteJid")
        message = msg_data.get("message", {})

        text = (
            message.get("conversation") or
            message.get("extendedTextMessage", {}).get("text") or
            message.get("imageMessage", {}).get("caption")
        )
        audio_msg = message.get("audioMessage")

        if text:
            background_tasks.add_task(process_and_respond, remote_jid, text)
        elif audio_msg:
            background_tasks.add_task(
                process_audio_and_respond, remote_jid, audio_msg
            )

    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
