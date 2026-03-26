import os
from unittest.mock import MagicMock
from src.rag_engine import get_rag_engine
from llama_index.core.schema import NodeWithScore, TextNode

def test_darija_quality():
    # Mocking components
    engine = get_rag_engine(use_auto_retriever=False)
    
    # Mock some products
    nodes = [
        NodeWithScore(node=TextNode(text="HP Elitebook X360 G2, Core i5 7th Gen, 8GB RAM, 256GB SSD, 13.3 Touch Screen.", metadata={"name": "HP Elitebook X360 G2", "price": "3500 Dhs", "url": "http://jumia.com/hp"}), score=0.9),
        NodeWithScore(node=TextNode(text="Dell Latitude 7490, Core i7 8th Gen, 16GB RAM, 512GB SSD, 14 FHD.", metadata={"name": "Dell Latitude 7490", "price": "4800 Dhs", "url": "http://jumia.com/dell"}), score=0.85),
    ]
    
    # Synthesize response
    query = "Salam, bghit chi laptop mkhyr l-khdma."
    response = engine._response_synthesizer.synthesize(query=query, nodes=nodes)
    
    print("\n--- DARIJA TEST OUTPUT ---")
    print(response.response)
    print("--------------------------")

if __name__ == "__main__":
    test_darija_quality()
