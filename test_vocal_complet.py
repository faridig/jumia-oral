import os
import logging
import sys
from src.voice import transcribe_audio
from src.rag_engine import MultiQueryAutoRAG
from dotenv import load_dotenv

# Silence technique pour la démo
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("test_vocal")
logger.setLevel(logging.INFO)

load_dotenv()

def test_vocal_reel(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Erreur : Le fichier '{file_path}' est introuvable.")
        print("Veuillez placer votre fichier audio (mp3, ogg, wav) dans le dossier du projet.")
        return

    print(f"\n--- 🎙️ 1. TRANSCRIPTION WHISPER (DARIJA-NATIVE) ---")
    text = transcribe_audio(file_path)
    
    if not text:
        print("❌ Échec de la transcription Whisper. Vérifiez votre clé OPENAI_API_KEY.")
        return
        
    print(f"✅ Texte reconnu : \"{text}\"")

    print(f"\n--- 🧠 2. RECHERCHE RAG JUMIA ---")
    rag = MultiQueryAutoRAG()
    # On simule l'appel de l'agent
    response = rag.query(text)
    
    print("\n--- 🇲🇦 3. RÉPONSE DU BOT (DARIJA-NATIVE) ---")
    if hasattr(response, 'response'):
        print(response.response)
    else:
        print(response)

if __name__ == "__main__":
    audio_file = sys.argv[1] if len(sys.argv) > 1 else "mon_test.mp3"
    test_vocal_reel(audio_file)
