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
        "Had l-PC HP EliteBook mkhyr l-khidma, taman dyalou rbe3 alaf o khms mtya d-derhem.\n"
        "[/TTS]"
    )
    
    parsed = manager._parse_multimodal_response(raw_llm_text)
    
    assert "💻 HP EliteBook" in parsed["text_whatsapp"]
    assert "https://jumia.ma/hp-elitebook" in parsed["text_whatsapp"]
    assert "Had l-PC HP EliteBook" in parsed["text_tts"]
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
