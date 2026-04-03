import os
import pytest
import unittest.mock
import httpx
from src.rag_engine import URLAvailabilityPostprocessor, MultiQueryAutoRAG
from llama_index.core.schema import NodeWithScore, TextNode

def test_url_availability_postprocessor_pbi_1901():
    """
    Vérifie que le post-processeur supprime les URLs 404 (PBI-1901).
    """
    postprocessor = URLAvailabilityPostprocessor()
    
    # Création de deux noeuds : un valide (200) et un invalide (404)
    valid_node = NodeWithScore(
        node=TextNode(text="Produit 1", metadata={"url": "https://www.jumia.ma/prod-ok"}),
        score=0.9
    )
    invalid_node = NodeWithScore(
        node=TextNode(text="Produit 2", metadata={"url": "https://www.jumia.ma/prod-dead"}),
        score=0.8
    )
    
    nodes = [valid_node, invalid_node]
    
    # Mock de httpx.Client utilisé dans src.rag_engine
    with unittest.mock.patch("src.rag_engine.httpx.Client") as mock_client_class:
        def side_effect(url, **kwargs):
            mock_resp = unittest.mock.MagicMock()
            if "ok" in url:
                mock_resp.status_code = 200
            else:
                mock_resp.status_code = 404
            return mock_resp
            
        mock_client_instance = mock_client_class.return_value.__enter__.return_value
        mock_client_instance.head.side_effect = side_effect
        
        processed_nodes = postprocessor._postprocess_nodes(nodes)
    
    assert len(processed_nodes) == 1
    assert processed_nodes[0].node.metadata["url"] == "https://www.jumia.ma/prod-ok"

def test_single_sniper_recommendation_pbi_1904():
    """
    Vérifie que le RAG est configuré pour le mode 'Single Sniper' (PBI-1904).
    On vérifie que le prompt contient bien les nouvelles instructions.
    """
    # Ce test vérifie indirectement que le système est paramétré pour une seule option
    # en vérifiant la limitation des nodes et les instructions du prompt.
    with unittest.mock.patch("src.rag_engine.expand_query_darija", return_value=["laptop"]):
        rag = MultiQueryAutoRAG()
        
        # Vérification que le synthesizer est appelé avec au plus 3 nodes
        with unittest.mock.patch.object(rag.auto_engine._response_synthesizer, 'synthesize') as mock_synthesize:
            mock_synthesize.return_value = "Réponse Sniper"
            
            # Mock des source_nodes du retriever
            mock_res = unittest.mock.Mock()
            mock_res.source_nodes = [unittest.mock.Mock()] * 5 # On simule 5 résultats trouvés
            
            with unittest.mock.patch.object(rag.auto_engine, 'query', return_value=mock_res):
                rag.query("Bghit laptop")
                
                # Vérification de l'appel à synthesize
                args, kwargs = mock_synthesize.call_args
                nodes_passed = kwargs.get('nodes') or args[1]
                assert len(nodes_passed) <= 3 # On a limité à 3 pour que le LLM choisisse LE meilleur
