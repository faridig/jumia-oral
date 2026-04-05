import os
import logging
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_multimodal_response(user_query: str, context_nodes: list, chat_history: list = None) -> dict:
    """
    Génère une réponse multimodale (Texte + Audio natif) via GPT-4o Audio Preview.
    Garantit une prosodie Casablancaise authentique et un timbre 'Marin' (PR #30).
    """
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY non configurée pour GPT-4o Audio.")
        return None

    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # 1. Préparation du contexte technique (Sniper Strategy)
    context_text = "\n".join([
        f"Produit: {n.node.metadata.get('name')}\nPrix: {n.node.metadata.get('price_numeric')} MAD\nSpecs: {n.node.metadata.get('description')}\nURL: {n.node.metadata.get('url')}"
        for n in context_nodes
    ])
    
    # 2. Historique conversationnel
    history_text = ""
    if chat_history:
        history_text = "\n".join([f"{m.role}: {m.content}" for m in chat_history[-5:]])

    # 3. Système Prompt CASA avec injection de prosodie native (PR #30)
    system_prompt = (
        "Tu es le 'Compagnon Notebook Jumia', un vendeur expert à Casablanca (Derb Ghalef style).\n"
        "INSTRUCTION DE PROSODIE : Speak as a warm, persuasive Moroccan personal shopper from Casablanca. "
        "Use natural Darija intonations, emphasize 'hemza' (good deals), and maintain a complicit, helpful tone. "
        "Avoid any robotic or monotone delivery.\n\n"
        "CONSIGNES :\n"
        "1. Choisis LE MEILLEUR produit parmi les nodes fournis.\n"
        "2. Ton texte de sortie (modality text) doit être le message WhatsApp minimaliste : *NOM* - *PRIX* MAD \n\n Khoudou mn hna : [URL]\n"
        "3. Ton audio de sortie (modality audio) doit être ton conseil chaleureux en Darija Casa, incluant les specs techniques de manière fluide.\n"
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": "marin", "format": "opus"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": f"CONTEXTE TECHNIQUE (NODES):\n{context_text}"},
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
    Génère un fichier audio .opus via OpenAI TTS (PBI-1701.1).
    Utilise le modèle tts-1 pour une synthèse ultra-rapide (<1s).
    Voix recommandée (Maroc/Darija) : marin (warm & persuasive).
    """
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY non configurée pour la synthèse vocale.")
        return None

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        # Voix supportées : alloy, echo, fable, onyx, nova, shimmer, ash, sage, coral, marin, cedar.
        # Note : marin est le timbre original validé pour le marché marocain (PBI-1701.1).
        
        # PBI-1701.1 Scenario 1 & 2
        response = client.audio.speech.create(
            model="tts-1",
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
