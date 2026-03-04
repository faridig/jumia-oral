import pytest
from src.rag_engine import MultiQueryAutoRAG
from unittest.mock import patch, MagicMock

@pytest.fixture
def rag_engine():
    return MultiQueryAutoRAG()

def test_comparison_detection():
    rag = MultiQueryAutoRAG()
    # Test internal logic by mocking dependencies
    with patch.object(rag.auto_engine, 'query') as mock_query:
        # Create mock source nodes
        node1 = MagicMock()
        node1.node.metadata = {"name": "Product 1", "price_numeric": 1000, "trust_score": 4.5, "value_for_money_score": 8.0}
        node1.node.get_content.return_value = "Product 1 details"
        
        node2 = MagicMock()
        node2.node.metadata = {"name": "Product 2", "price_numeric": 1200, "trust_score": 4.0, "value_for_money_score": 7.0}
        node2.node.get_content.return_value = "Product 2 details"
        
        mock_response = MagicMock()
        mock_response.source_nodes = [node1, node2]
        mock_query.return_value = mock_response
        
        with patch("src.rag_engine.get_response_synthesizer") as mock_synth_gen:
            mock_synthesizer = MagicMock()
            mock_synthesizer.synthesize.return_value = "Comparison Table Result"
            mock_synth_gen.return_value = mock_synthesizer
            
            result = rag.query("Lequel est le meilleur entre Product 1 et Product 2 ?")
            
            assert result == "Comparison Table Result"
            mock_synth_gen.assert_called()
            # Verify it used the comparison prompt
            args, kwargs = mock_synth_gen.call_args
            assert "tableau Markdown" in kwargs["text_qa_template"].template
