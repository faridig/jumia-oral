
import os
import sys
from src.rag_engine import MultiQueryAutoRAG

def test_tts_format():
    print("Démarrage du test RAG Engine pour le format TTS...")
    rag = MultiQueryAutoRAG()
    query = "Bghit chi laptop mkhyr l-khidma"
    response = rag.query(query)
    
    response_text = str(response)
    print("\n--- RÉPONSE BRUTE ---")
    print(response_text)
    print("----------------------\n")
    
    if "[WHATSAPP]" in response_text and "[/WHATSAPP]" in response_text:
        print("✅ Balises [WHATSAPP] présentes.")
    else:
        print("❌ Balises [WHATSAPP] manquantes.")
        
    if "[TTS]" in response_text and "[/TTS]" in response_text:
        print("✅ Balises [TTS] présentes.")
        # Extraction du texte TTS
        tts_content = response_text.split("[TTS]")[1].split("[/TTS]")[0].strip()
        print(f"Contenu TTS extrait : {tts_content}")
        
        # Vérification simpliste des caractères arabes (range \u0600-\u06FF)
        has_arabic = any('\u0600' <= char <= '\u06FF' for char in tts_content)
        if has_arabic:
            print("✅ Le bloc [TTS] contient des caractères ARABES.")
        else:
            print("❌ Le bloc [TTS] ne contient PAS de caractères ARABES.")
    else:
        print("❌ Balises [TTS] manquantes.")

if __name__ == "__main__":
    test_tts_format()
