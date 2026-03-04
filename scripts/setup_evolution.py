import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://localhost:8080")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "apikey")
INSTANCE_NAME = os.getenv("INSTANCE_NAME", "jumia")

def setup_instance():
    print(f"--- Configuration de l'instance Evolution API : {INSTANCE_NAME} ---")
    
    # 1. Vérifier si l'instance existe
    url_fetch = f"{EVOLUTION_API_URL}/instance/fetchInstances"
    headers = {"apikey": EVOLUTION_API_KEY}
    
    try:
        response = requests.get(url_fetch, headers=headers)
        instances = response.json()
        
        instance_exists = any(inst.get("instanceName") == INSTANCE_NAME for inst in instances) if isinstance(instances, list) else False
        
        if instance_exists:
            print(f"✅ L'instance '{INSTANCE_NAME}' existe déjà.")
        else:
            print(f"🟡 Création de l'instance '{INSTANCE_NAME}'...")
            url_create = f"{EVOLUTION_API_URL}/instance/create"
            payload = {
                "instanceName": INSTANCE_NAME,
                "token": EVOLUTION_API_KEY,
                "number": "",
                "qrcode": True
            }
            res = requests.post(url_create, json=payload, headers=headers)
            if res.status_code == 201:
                print(f"✅ Instance '{INSTANCE_NAME}' créée avec succès.")
            else:
                print(f"❌ Échec de la création : {res.text}")
                return
        
        # 2. Configurer le Webhook
        print(f"🟡 Configuration du Webhook...")
        url_webhook = f"{EVOLUTION_API_URL}/webhook/set/{INSTANCE_NAME}"
        webhook_payload = {
            "enabled": True,
            "url": "http://host.docker.internal:5000/webhook", # Ajuster selon l'env
            "webhook_by_events": False,
            "events": [
                "MESSAGES_UPSERT"
            ]
        }
        res_webhook = requests.post(url_webhook, json=webhook_payload, headers=headers)
        if res_webhook.status_code == 201:
            print(f"✅ Webhook configuré vers http://host.docker.internal:5000/webhook")
        else:
            print(f"❌ Échec de la configuration du Webhook : {res_webhook.text}")

    except Exception as e:
        print(f"❌ Erreur lors du setup: {e}")

if __name__ == "__main__":
    setup_instance()
