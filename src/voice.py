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
    user_query: str, context_nodes: list, chat_history: list = None, intent: str = "PRODUCT"
) -> dict:
    """
    Génère une réponse multimodale (Texte + Audio natif).
    """
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY non configurée pour GPT-4o Audio.")
        return None

    client = OpenAI(api_key=OPENAI_API_KEY)

    # 1. Préparation du contexte technique (Enrichi avec Rationale - PBI-31 Fix)
    nodes_info = []
    for n in context_nodes:
        m = n.node.metadata
        # On récupère le contenu brut (qui contient l'analyse de sentiment et les specs)
        content = n.node.get_content()
        nodes_info.append(
            f"PRODUIT: {m.get('name')}\n"
            f"PRIX: {m.get('price_numeric')} MAD\n"
            f"URL: {m.get('url')}\n"
            f"DÉTAILS SÉMANTIQUES:\n{content}"
        )
    context_text = "\n---\n".join(nodes_info)

    # 2. Historique conversationnel
    history_text = ""
    if chat_history:
        history_text = "\n".join([f"{m.role}: {m.content}" for m in chat_history[-5:]])

    # 3. Système Prompt CASA (Séparation Prosodie vs Structure - PBI-31 Fix)
    system_prompt = (
        "Tu es le 'Compagnon Notebook Jumia', un vendeur expert à Casablanca.\n"
        "Tu fournis DEUX flux distincts : un message TEXTE pour WhatsApp et un message AUDIO.\n\n"
        "PROSODIE AUDIO (STRICTE) :\n"
        "- Parle comme un 'Personal Shopper' marocain chaleureux et persuasif (Darija de Casablanca).\n"
        "- Salue toujours l'utilisateur au début de la conversation ou si la requête est une salutation.\n"
        "- INTERDICTION FORMELLE de prononcer l'URL, de dire 'cliquez sur le lien' ou d'épeler des caractères techniques.\n"
        "- Ne cite pas les prix de manière robotique. Dis par exemple : 'Hada gha b 5000 dirham, hemza khouya'.\n"
        "- Utilise un ton de conseil entre amis. Utilise des mots comme 'Madi', 'Tayra', 'Naddi', 'mkhyyer'.\n"
        "- Mentionne les specs (CPU, RAM, SSD) naturellement, sans lire une fiche technique.\n\n"
        "STRUCTURE TEXTE (WHATSAPP) :\n"
        "- C'est ton SEUL support pour le lien technique.\n"
        "- Format : *NOM DU PRODUIT* - *PRIX* MAD\n\nKhoudou mn hna : [URL]\n"
        "- INTERDICTION d'utiliser des puces ou du formattage complexe."
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

        message = completion.choices[0].message
        audio_data = base64.b64decode(message.audio.data)
        
        # Récupération de secours robuste (PBI-31 Fix)
        # Au lieu d'utiliser le transcript (qui doit être pur), on reconstruit le lien manuellement
        text_whatsapp = message.content
        if not text_whatsapp or text_whatsapp.strip() == "":
            # On ne force la reconstruction que si l'intention PRODUIT est confirmée (PBI-31 Fix)
            if context_nodes and "PRODUCT" in intent:
                best_node = context_nodes[0].node.metadata
                text_whatsapp = f"*{best_node.get('name')}* - {best_node.get('price_numeric')} MAD\n\nKhoudou mn hna : {best_node.get('url')}"
                logger.warning("Modèle paresseux : Reconstruction manuelle du lien WhatsApp.")
            else:
                text_whatsapp = message.audio.transcript
                logger.info("Utilisation du transcript car le contenu texte est vide ou intention non-produit.")

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
                response_format="text",
                prompt="C'est un message audio en Darija marocain (Casablanca) parlant de laptops Jumia, mkhyr, naddi, madi, PC, hemza."
            )
            return transcript
    except Exception as e:
        logger.error(f"Erreur Whisper: {e}")
        return None
