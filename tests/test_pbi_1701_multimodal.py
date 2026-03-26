import pytest
from src.session_manager import JumiaChatManager
from unittest.mock import MagicMock

def test_parse_multimodal_response_with_tags_arabizi():
    """
    Scenario 1 : Séparation des sorties (PBI-1701.3)
    Migration PR #24 : Le TTS doit être en Arabizi phonétique pour Casa.
    """
    manager = JumiaChatManager(storage_path="data/test_sessions.json")
    raw_llm_text = (
        "[WHATSAPP]\n"
        "*💻 HP EliteBook X360 G2*\n"
        "[Voir sur Jumia](https://jumia.ma/hp-elitebook)\n"
        "[/WHATSAPP]\n"
        "[TTS]\n"
        "Khouya sahbi, had l-bi si naddi bzaf, madi tayra f l-khidma.\n"
        "[/TTS]"
    )
    
    parsed = manager._parse_multimodal_response(raw_llm_text)
    
    assert "💻 HP EliteBook" in parsed["text_whatsapp"]
    # Vérifie l'Arabizi phonétique Casa
    assert "Khouya sahbi" in parsed["text_tts"]
    assert "naddi bzaf" in parsed["text_tts"]
    assert "[/WHATSAPP]" not in parsed["text_whatsapp"]
    assert "[TTS]" not in parsed["text_tts"]
    assert "💻" not in parsed["text_tts"]
