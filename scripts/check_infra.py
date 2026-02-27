import os
import requests
import time
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from openai import OpenAI

def check_qdrant(url, collection_name):
    print(f"--- Vérification Qdrant ({url}) ---")
    try:
        client = QdrantClient(url=url)
        # 1. Vérifier la connexion
        collections = client.get_collections()
        print(f"✅ Connexion Qdrant réussie.")
        
        # 2. Vérifier/Créer la collection
        collection_names = [c.name for c in collections.collections]
        if collection_name in collection_names:
            print(f"✅ Collection '{collection_name}' existe déjà.")
        else:
            print(f"🟡 Collection '{collection_name}' absente. Création...")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
            print(f"✅ Collection '{collection_name}' créée.")
        return True
    except Exception as e:
        print(f"❌ Erreur Qdrant : {e}")
        return False

def check_openai(api_key):
    print("--- Vérification OpenAI ---")
    if not api_key or "your_openai" in api_key:
        print("⚠️ OPENAI_API_KEY non configurée dans le .env.")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print("✅ Connexion OpenAI réussie.")
        return True
    except Exception as e:
        print(f"❌ Erreur OpenAI : {e}")
        return False

def check_evolution_api(url, api_key):
    print(f"--- Vérification Evolution API ({url}) ---")
    try:
        # Test de santé (root)
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("✅ Evolution API est accessible.")
            return True
        else:
            print(f"❌ Evolution API a répondu avec le statut : {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur Evolution API : {e}")
        return False

def main():
    load_dotenv()
    
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6343")
    qdrant_collection = os.getenv("QDRANT_COLLECTION_NAME", "jumia_products")
    openai_key = os.getenv("OPENAI_API_KEY")
    evo_url = os.getenv("EVOLUTION_API_URL", "http://localhost:8080")
    evo_key = os.getenv("EVOLUTION_API_KEY", "apikey")
    
    qdrant_ok = check_qdrant(qdrant_url, qdrant_collection)
    openai_ok = check_openai(openai_key)
    evo_ok = check_evolution_api(evo_url, evo_key)
    
    if qdrant_ok and openai_ok and evo_ok:
        print("\n🚀 Infrastructure Jumia Oral validée !")
    else:
        print("\n⚠️ Certaines vérifications ont échoué. Vérifiez vos variables d'environnement et vos containers.")

if __name__ == "__main__":
    main()
