import pytest
from src.rag_engine import MultiQueryAutoRAG
import unittest.mock as mock

@pytest.fixture
def rag_engine():
    return MultiQueryAutoRAG()

def test_pbi_2002_minimalist_whatsapp_format(rag_engine):
    # Mocking the synthesizer to return a fixed string with tags
    with mock.patch.object(rag_engine.auto_engine._response_synthesizer, 'synthesize') as mock_synthesize:
        mock_synthesize.return_value = mock.MagicMock(
            __str__=lambda x: "[WHATSAPP]\n*HP EliteBook 840* - *4500* MAD\n\nKhoudou mn hna : https://jumia.ma/hp-elitebook\n[/WHATSAPP]\n[TTS]\nSalam khouya, had l-HP madi w tayra...\n[/TTS]",
            source_nodes=[mock.MagicMock()]
        )
        
        # This is more of a unit test for the session manager parsing if we want to check extraction,
        # but here we want to check what the PROMPT produces.
        # Since I can't easily run a real LLM call here without an API key and it might be non-deterministic,
        # I will check if the PROMPT (the system_prompt string) contains the new instructions.
        
        from src.rag_engine import get_rag_engine
        engine = get_rag_engine()
        system_prompt = engine._response_synthesizer._llm.system_prompt
        
        # PBI-2002: Minimalist format
        assert "*NOM DU PRODUIT* - *PRIX* MAD" in system_prompt
        assert "Khoudou mn hna : [URL]" in system_prompt
        assert "Pas de puces" in system_prompt or "INTERDICTION" in system_prompt or "minimaliste" in system_prompt.lower()

def test_pbi_2003_audio_narration_instructions(rag_engine):
    from src.rag_engine import get_rag_engine
    engine = get_rag_engine()
    system_prompt = engine._response_synthesizer._llm.system_prompt
    
    # PBI-2003: Audio Phoenix metaphors and specs
    assert "Madi" in system_prompt
    assert "Tayra" in system_prompt
    assert "Naddi" in system_prompt
    assert "CPU" in system_prompt
    assert "RAM" in system_prompt
    assert "SSD" in system_prompt
