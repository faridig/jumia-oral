from src.rag_engine import MultiQueryAutoRAG
import os

def smoke_test():
    print("--- Lancement du Smoke Test ---")
    rag = MultiQueryAutoRAG()
    query = "Je cherche un PC portable pour du gaming avec 16Go de RAM"
    print(f"Requête : {query}")
    response = rag.query(query)
    print("\n--- Réponse du Bot ---")
    print(response)
    print("\n--- Sources ---")
    if hasattr(response, 'source_nodes'):
        for node in response.source_nodes[:2]:
            print(f"- {node.node.metadata.get('name', 'N/A')}")

if __name__ == "__main__":
    smoke_test()
