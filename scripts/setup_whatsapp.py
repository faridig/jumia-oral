import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://localhost:8080")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "apikey")
INSTANCE_NAME = os.getenv("INSTANCE_NAME", "Jumia-Oral-Agent")
# En production, cette URL serait fournie par Ngrok (ex: https://abc.ngrok-free.app/webhook)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:8000/webhook")

headers = {
    "apikey": EVOLUTION_API_KEY,
    "Content-Type": "application/json"
}

def create_instance():
    print(f"--- Création de l'instance {INSTANCE_NAME} ---")
    url = f"{EVOLUTION_API_URL}/instance/create"
    payload = {
        "instanceName": INSTANCE_NAME,
        "integration": "WHATSAPP-BAILEYS",
        "qrcode": True
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        data = response.json()
        print("Instance créée avec succès !")
        if "qrcode" in data:
            print("QR Code (Base64) disponible. Scannez-le pour connecter WhatsApp.")
            # print(data["qrcode"]["base64"])
    elif response.status_code == 403:
        print("L'instance existe peut-être déjà.")
    else:
        print(f"Erreur lors de la création : {response.text}")

def set_webhook():
    print(f"--- Configuration du Webhook pour {INSTANCE_NAME} ---")
    url = f"{EVOLUTION_API_URL}/webhook/set/{INSTANCE_NAME}"
    payload = {
        "webhook": {
            "enabled": True,
            "url": WEBHOOK_URL,
            "byEvents": True,
            "base64": True,
            "events": [
                "MESSAGES_UPSERT",
                "CONNECTION_UPDATE",
                "QRCODE_UPDATED"
            ]
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code in [200, 201]:
        print(f"Webhook configuré sur {WEBHOOK_URL}")
    else:
        # Si ça échoue, on tente la structure plate
        print(f"Échec avec structure imbriquée. Tentative structure plate...")
        payload_flat = {
            "enabled": True,
            "url": WEBHOOK_URL,
            "webhookByEvents": True,
            "webhookBase64": True,
            "events": [
                "MESSAGES_UPSERT",
                "CONNECTION_UPDATE",
                "QRCODE_UPDATED"
            ]
        }
        response = requests.post(url, json=payload_flat, headers=headers)
        if response.status_code in [200, 201]:
             print(f"Webhook configuré sur {WEBHOOK_URL} (structure plate)")
        else:
             print(f"Erreur lors de la configuration du webhook : {response.text}")

if __name__ == "__main__":
    create_instance()
    set_webhook()
