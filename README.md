# 👑 Jumia RAG Assistant - WhatsApp (MVP)

## 🎯 Vision du Projet
Transformer le catalogue informatique de **Jumia.ma** en un assistant personnel de shopping conversationnel sur **WhatsApp**. L'assistant utilise le **RAG (Retrieval-Augmented Generation)** pour conseiller, comparer et recommander les meilleurs produits aux utilisateurs marocains avec un ton amical et local.

## ⚙️ Stack Technique
- **Scraping** : [Crawl4AI](https://crawl4ai.com/) + LLM Extraction (GPT-4o-mini).
- **IA Orchestration** : [LlamaIndex](https://www.llamaindex.ai/).
- **Vector DB** : [Qdrant](https://qdrant.tech/) (Recherche hybride Dense/Sparse).
- **WhatsApp** : [Evolution API](https://evolution-api.com/) (Open Source).
- **Backend** : FastAPI (Python 3.12+).

## 📂 Organisation du Projet
- `docs/` : Documentation de conception (Backlog, Sprints, Ton).
- `src/` : Code source (Scraper, Indexeur, API).
- `scripts/` : Scripts utilitaires (Infrastructure, Migration).
- `data/raw/markdown/` : Catalogue produit extrait.
- `logs/` : Traces d'exécution.

## 🚀 Installation & Développement

### 1. Prérequis
- Python 3.12+
- Docker & Docker Compose

### 2. Initialisation de l'environnement
```bash
# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration
Copiez le fichier d'exemple et remplissez vos clés API :
```bash
cp .env.example .env
```

### 4. Lancement de l'infrastructure
L'infrastructure utilise une instance Qdrant existante. Si vous n'en avez pas, lancez-en une :
```bash
docker run -d --name jumia_qdrant -p 6343:6333 -p 6344:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant:latest
```

Ensuite, lancez Evolution API (WhatsApp) :
```bash
docker compose up -d
```
Les services seront accessibles :
- **Qdrant** : [http://localhost:6343/dashboard](http://localhost:6343/dashboard)
- **Evolution API** : [http://localhost:8080](http://localhost:8080)

### 5. Vérification
Exécutez le script de diagnostic :
```bash
python scripts/check_infra.py
```

## 🇲🇦 Personnalité
L'assistant parle un français chaleureux avec des touches de **Darija** (Mrehba, Besseha, Chouf), agissant comme un expert de confiance ("Personal Shopper").

---
*Projet en cours de développement (Sprint 0 - Infrastructure).*
# Dummy
