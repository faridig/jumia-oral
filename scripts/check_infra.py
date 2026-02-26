import os
import requests
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from openai import OpenAI

def check_qdrant(url):
    print(f"--- Vérification Qdrant ({url}) ---")
    try:
        # On utilise l'URL mappée sur l'hôte
        client = QdrantClient(url=url)
        # Test simple : récupérer les collections
        collections = client.get_collections()
        print(f"✅ Connexion Qdrant réussie. Collections : {collections}")
        return True
    except Exception as e:
        print(f"❌ Erreur Qdrant : {e}")
        return False

def check_openai(api_key):
    print("--- Vérification OpenAI ---")
    if not api_key or "your_openai" in api_key:
        print("⚠️ OPENAI_API_KEY non configurée ou valeur par défaut.")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print(f"✅ Connexion OpenAI réussie. Réponse : {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ Erreur OpenAI : {e}")
        return False

def main():
    load_dotenv()
    
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6343")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    qdrant_ok = check_qdrant(qdrant_url)
    openai_ok = check_openai(openai_key)
    
    if qdrant_ok and openai_ok:
        print("\n🚀 Infrastructure validée !")
    else:
        print("\n⚠️ Certaines vérifications ont échoué. Vérifiez vos variables d'environnement et vos containers.")

if __name__ == "__main__":
    main()
