#!/bin/bash

# 🦁 Jumia Oral Control Panel (PBI-2101)
# Ce script gère le cycle de vie complet du projet Jumia Oral.

# Configuration
ENV_FILE=".env"
FASTAPI_PORT=8000
NGROK_PORT=$FASTAPI_PORT
LOG_DIR="logs"
PYTHON_BIN="./venv/bin/python3"

# Création du dossier de logs si absent
mkdir -p "$LOG_DIR"

# Chargement manuel des variables d'environnement nécessaires
if [ -f "$ENV_FILE" ]; then
    # On exporte uniquement ce dont on a besoin pour éviter les conflits
    EVOLUTION_API_URL=$(grep "^EVOLUTION_API_URL=" "$ENV_FILE" | cut -d'=' -f2)
    EVOLUTION_API_KEY=$(grep "^EVOLUTION_API_KEY=" "$ENV_FILE" | cut -d'=' -f2)
    INSTANCE_NAME=$(grep "^INSTANCE_NAME=" "$ENV_FILE" | cut -d'=' -f2)
fi

# Valeurs par défaut si absentes du .env
EVOLUTION_API_URL=${EVOLUTION_API_URL:-"http://localhost:8080"}
EVOLUTION_API_KEY=${EVOLUTION_API_KEY:-"apikey"}
INSTANCE_NAME=${INSTANCE_NAME:-"Jumia-Oral-Agent"}

start() {
    echo "🚀 Démarrage des services Jumia Oral..."

    # 1. Start Docker Containers
    echo "📦 [1/5] Lancement de Qdrant et Evolution API via Docker Compose..."
    docker compose up -d
    
    # 2. Start FastAPI
    echo "🐍 [2/5] Lancement du serveur FastAPI (Uvicorn)..."
    pkill -f "uvicorn src.api:app" 2>/dev/null
    nohup "$PYTHON_BIN" -m uvicorn src.api:app --host 0.0.0.0 --port $FASTAPI_PORT > "$LOG_DIR/fastapi.log" 2>&1 &
    
    # Attente pour que FastAPI soit prêt
    sleep 2
    
    # 3. Start Localtunnel
    echo "🌐 [3/5] Lancement du tunnel Localtunnel sur le port $FASTAPI_PORT..."
    # Nettoyage d'éventuels processus orphelins
    pkill -f "npx --yes localtunnel" 2>/dev/null
    # Localtunnel en arrière-plan
    npx --yes localtunnel --port $FASTAPI_PORT > "$LOG_DIR/localtunnel.log" 2>&1 &
    
    # Attente de l'URL Localtunnel (max 30s)
    echo -n "⏳ Récupération de l'URL publique Localtunnel..."
    MAX_RETRIES=15
    COUNT=0
    TUNNEL_URL=""
    while [ $COUNT -lt $MAX_RETRIES ]; do
        if grep -q "your url is:" "$LOG_DIR/localtunnel.log"; then
            TUNNEL_URL=$(grep "your url is:" "$LOG_DIR/localtunnel.log" | awk '{print $4}')
            echo " OK"
            break
        fi
        echo -n "."
        # Check if localtunnel process is still alive
        if ! pgrep -f "localtunnel" > /dev/null; then
            echo -e "\n❌ Localtunnel s'est arrêté prématurément. Vérifiez logs/localtunnel.log"
            exit 1
        fi
        sleep 2
        ((COUNT++))
    done

    if [ -z "$TUNNEL_URL" ]; then
        echo -e "\n❌ Échec : Impossible de récupérer l'URL Localtunnel."
        exit 1
    fi
    echo "🔗 URL Tunnel active : $TUNNEL_URL"

    # 4. Update .env
    echo "📝 [4/5] Mise à jour de WEBHOOK_URL dans $ENV_FILE..."
    FULL_WEBHOOK_URL="${TUNNEL_URL}/webhook"
    
    # Utilisation de sed pour mettre à jour ou ajouter la variable
    if grep -q "^WEBHOOK_URL=" "$ENV_FILE"; then
        # Version Linux compatible sed -i
        sed -i "s|^WEBHOOK_URL=.*|WEBHOOK_URL=\"$FULL_WEBHOOK_URL\"|" "$ENV_FILE"
    else
        echo "WEBHOOK_URL=\"$FULL_WEBHOOK_URL\"" >> "$ENV_FILE"
    fi

    # 5. Update Evolution API Webhook
    echo "🔌 [5/5] Synchronisation du Webhook dans l'instance Evolution API ($INSTANCE_NAME)..."
    
    # On attend que l'API Evolution réponde avant de configurer
    MAX_API_RETRIES=10
    API_COUNT=0
    while [ $API_COUNT -lt $MAX_API_RETRIES ]; do
        if curl -s "$EVOLUTION_API_URL/instance/fetchInstances" -H "apikey: $EVOLUTION_API_KEY" > /dev/null; then
            break
        fi
        sleep 2
        ((API_COUNT++))
    done

    CURL_RESPONSE=$(curl -s -X POST "$EVOLUTION_API_URL/webhook/set/$INSTANCE_NAME" \
      -H "Content-Type: application/json" \
      -H "apikey: $EVOLUTION_API_KEY" \
      -d "{
        \"webhook\": {
          \"enabled\": true,
          \"url\": \"$FULL_WEBHOOK_URL\",
          \"byEvents\": false,
          \"base64\": true,
          \"events\": [\"MESSAGES_UPSERT\"]
        }
      }")
    
    if echo "$CURL_RESPONSE" | grep -q "\"status\":\"SUCCESS\"" || echo "$CURL_RESPONSE" | grep -q "\"error\":false" || echo "$CURL_RESPONSE" | grep -q "\"id\""; then
        echo "✅ Webhook synchronisé avec succès."
    else
        echo "⚠️  Attention : Le webhook n'a peut-être pas été mis à jour dans Evolution API. Réponse: $CURL_RESPONSE"
    fi
    
    echo -e "\n🎉 Tous les services sont opérationnels !"
    echo "🌐 FastAPI : http://localhost:$FASTAPI_PORT"
    echo "📡 Webhook  : $FULL_WEBHOOK_URL"
    echo "📊 Logs dispos dans le dossier $LOG_DIR/"
}

stop() {
    echo "🛑 Arrêt des services Jumia Oral..."
    
    echo "🐍 Arrêt de FastAPI..."
    pkill -f "uvicorn src.api:app"
    
    echo "🌐 Arrêt de Localtunnel..."
    pkill -f "localtunnel"
    
    echo "📦 Arrêt des conteneurs Docker..."
    docker compose stop
    
    echo "✅ Tous les services ont été stoppés."
}

status() {
    echo "----------------------------------------"
    echo "📊 État des services Jumia Oral :"
    echo "----------------------------------------"
    
    # Check Docker
    echo -n "📦 Docker Containers : "
    EVO_RUNNING=$(docker ps -q --filter "name=jumia_evolution_api")
    QDRANT_RUNNING=$(docker ps -q --filter "name=qdrant_jumia")
    
    if [ -n "$EVO_RUNNING" ] && [ -n "$QDRANT_RUNNING" ]; then
        echo "🟢 UP"
    else
        [ -z "$EVO_RUNNING" ] && echo -n "🔴 Evolution API DOWN "
        [ -z "$QDRANT_RUNNING" ] && echo -n "🔴 Qdrant DOWN"
        echo ""
    fi
    
    # Check FastAPI
    echo -n "🐍 FastAPI Server   : "
    if pgrep -f "uvicorn src.api:app" > /dev/null; then
        echo "🟢 UP (Port $FASTAPI_PORT)"
    else
        echo "🔴 DOWN"
    fi
    
    # Check Tunnel
    echo -n "🌐 Localtunnel      : "
    if [ -f "$LOG_DIR/localtunnel.log" ] && grep -q "your url is:" "$LOG_DIR/localtunnel.log" && pgrep -f "localtunnel" > /dev/null; then
        TUNNEL_URL=$(grep "your url is:" "$LOG_DIR/localtunnel.log" | tail -1 | awk '{print $4}')
        echo "🟢 UP ($TUNNEL_URL)"
    else
        echo "🔴 DOWN"
        TUNNEL_URL=""
    fi
    
    # Check .env consistency
    ENV_URL=$(grep "^WEBHOOK_URL=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"')
    echo "📝 Webhook (.env)    : $ENV_URL"
    
    if [ -n "$TUNNEL_URL" ] && [ "${TUNNEL_URL}/webhook" != "$ENV_URL" ]; then
        echo "⚠️  DÉSYNCHRONISATION : L'URL du tunnel ne correspond pas au .env !"
    fi
    echo "----------------------------------------"
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|status}"
        exit 1
        ;;
esac
