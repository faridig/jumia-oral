import pytest
from src.session_manager import JumiaChatManager
from unittest.mock import MagicMock

def test_parse_multimodal_response_with_tags():
    """
    Scenario 1 : Séparation des sorties (PBI-1701.3)
    """
    manager = JumiaChatManager(storage_path="data/test_sessions.json")
    raw_llm_text = (
        "[WHATSAPP]\n"
        "*💻 HP EliteBook X360 G2*\n"
        "- Prix: 4500 Dhs\n"
        "[Voir sur Jumia](https://jumia.ma/hp-elitebook)\n"
        "[/WHATSAPP]\n"
        "[TTS]\n"
        "هاد البي سي إتش بي إليتبوك مخير للخدمة، الثمن ديالو أربعة آلاف وخمس مية درهم.\n"
        "[/TTS]"
    )
    
    parsed = manager._parse_multimodal_response(raw_llm_text)
    
    assert "💻 HP EliteBook" in parsed["text_whatsapp"]
    assert "https://jumia.ma/hp-elitebook" in parsed["text_whatsapp"]
    # Vérifie le script arabe pour le TTS (Correction post-rejet UX)
    assert "هاد البي سي" in parsed["text_tts"]
    assert "[/WHATSAPP]" not in parsed["text_whatsapp"]
    assert "[TTS]" not in parsed["text_tts"]
    assert "💻" not in parsed["text_tts"]

def test_parse_multimodal_response_fallback():
    """
    Scenario 1 : Séparation des sorties (PBI-1701.3) - Cas sans balises
    """
    manager = JumiaChatManager(storage_path="data/test_sessions.json")
    raw_llm_text = "Had l-PC madi bzaaf 🚀"
    
    parsed = manager._parse_multimodal_response(raw_llm_text)
    
    assert parsed["text_whatsapp"] == "Had l-PC madi bzaaf 🚀"
    # Le fallback doit enlever l'emoji pour le TTS
    assert "🚀" not in parsed["text_tts"]
