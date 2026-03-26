import os
import logging
import requests
import base64
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from pydantic import BaseModel
import tempfile
from src.session_manager import JumiaChatManager
from src.voice import transcribe_audio, generate_speech
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

from typing import Optional

def send_whatsapp_message(number: str, text: str, media_url: Optional[str] = None):
    """Envoie un message texte ou média (image) via Evolution API."""
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
        logger.info(f"Message envoyé à {number}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message: {e}")

def send_whatsapp_audio(number: str, audio_content: bytes):
    """Envoie un message vocal (.opus) via Evolution API."""
    url = f"{EVOLUTION_API_URL}/message/sendWhatsAppAudio/{INSTANCE_NAME}"
    
    # Encodage en base64 pour éviter le stockage disque temporaire (PBI-1701.2)
    audio_base64 = base64.b64encode(audio_content).decode('utf-8')
    data_uri = f"data:audio/ogg;base64,{audio_base64}"
    
    payload = {
        "number": number.split("@")[0],
        "audio": data_uri,
        "delay": 1200
    }
    
    headers = {
        "Content-Type": "application/json",
        "apikey": EVOLUTION_API_KEY
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logger.info(f"Audio envoyé à {number}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'audio: {e}")

def process_and_respond(user_id: str, text: str):
    logger.info(f"Début du traitement pour {user_id}")
    chat_response = get_chat_manager().handle_message(user_id, text)
    logger.info(f"Réponse RAG générée pour {user_id}")
    
    if isinstance(chat_response, dict):
        response_text = chat_response.get("text", "")
        text_tts = chat_response.get("text_tts", response_text)
        media_url = chat_response.get("media_url")
        
        # PBI-1701.2 UX : Séquençage Multimédia & Orchestration
        # 1. Envoi de l'image en premier (si disponible)
        if media_url:
            logger.info(f"1/3 Envoi de l'image à {user_id}")
            send_whatsapp_message(user_id, "", media_url)
        
        # 2. Envoi du texte WhatsApp (riche avec liens)
        logger.info(f"2/3 Envoi du texte WhatsApp à {user_id}")
        send_whatsapp_message(user_id, response_text)
        
        # 3. Envoi du message vocal généré par OpenAI Native Audio (gpt-4o-audio-preview)
        logger.info(f"3/3 Génération et envoi du vocal à {user_id}")
        audio_content = generate_speech(text_tts)
        if audio_content:
            send_whatsapp_audio(user_id, audio_content)
    else:
        # Fallback si ce n'est pas un dictionnaire
        logger.info(f"Envoi du message (fallback) à {user_id}")
        send_whatsapp_message(user_id, str(chat_response))

def download_media(url: str):
    headers = {"apikey": EVOLUTION_API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content

def process_audio_and_respond(user_id: str, audio_msg: dict):
    url = audio_msg.get("url")
    if not url:
        logger.error(f"Pas d'URL dans audioMessage pour {user_id}")
        return
    
    try:
        audio_data = download_media(url)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
            tmp.write(audio_data)
            tmp_path = tmp.name
        
        logger.info(f"Fichier audio téléchargé: {tmp_path}")
        text = transcribe_audio(tmp_path)
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        
        if text:
            logger.info(f"Audio transcrit pour {user_id}: {text}")
            process_and_respond(user_id, text)
        else:
            logger.error(f"Échec de la transcription pour {user_id}")
            send_whatsapp_message(user_id, "Sm7 lya, ma-9dertch n-sm3 l-message vocal dyalk mzyan. Te9der t-3awed t-siftou?")
            
    except Exception as e:
        logger.error(f"Erreur lors du traitement audio: {e}")

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    # Vérification de l'apikey dans les headers pour sécuriser la réception (PBI-803)
    provided_key = request.headers.get("apikey")
    if provided_key != EVOLUTION_API_KEY:
        logger.warning(f"Tentative d'accès non autorisée avec l'apikey: {provided_key}")
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()
    logger.info(f"Webhook reçu: {data.get('event')}")
    
    if data.get("event") == "messages.upsert":
        msg_data = data.get("data", {})
        key = msg_data.get("key", {})
        from_me = key.get("fromMe", False)
        
        if from_me:
            return {"status": "ignored", "reason": "message from self"}
        
        remote_jid = key.get("remoteJid")
        message = msg_data.get("message", {})
        
        # Extraction du contenu (Texte ou Audio)
        text = (
            message.get("conversation") or 
            message.get("extendedTextMessage", {}).get("text") or
            message.get("imageMessage", {}).get("caption") or
            message.get("videoMessage", {}).get("caption")
        )
        audio_msg = message.get("audioMessage")
        
        if text:
            # Traitement asynchrone (BackgroundTasks) pour répondre immédiatement 200 OK
            background_tasks.add_task(process_and_respond, remote_jid, text)
        elif audio_msg:
            # Traitement Audio (Whisper)
            background_tasks.add_task(process_audio_and_respond, remote_jid, audio_msg)
            
    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
