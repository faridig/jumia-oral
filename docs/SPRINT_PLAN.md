# 🏃 SPRINT PLAN - SPRINT 0 (INFRASTRUCTURE)

## 🎯 OBJECTIF
Mettre en place l'environnement de développement et valider la connexion à l'infrastructure existante (Qdrant).

## 📋 TÂCHES À RÉALISER

### [PBI-000] Initialisation de l'Espace de Travail
- **Tâches** :
  - [ ] Créer l'arborescence : `src/`, `scripts/`, `data/raw/markdown/`, `docs/`, `logs/`.
  - [ ] Créer `requirements.txt` (Crawl4ai, LlamaIndex, Qdrant-client, FastAPI, python-dotenv).
  - [ ] Créer `.env.example` avec :
    - `QDRANT_URL` (URL de votre instance existante)
    - `QDRANT_COLLECTION_NAME=jumia_products`
    - `OPENAI_API_KEY`
    - `EVOLUTION_API_KEY`

### [PBI-001] Infrastructure WhatsApp (Evolution API)
- **Tâches** :
  - [ ] Créer un fichier `docker-compose.yml` uniquement pour **Evolution API** (car Qdrant est déjà présent).
  - [ ] Lancer le container Evolution API et vérifier l'accès au port 8080.

### [PBI-002] Validation de la Chaîne de Connexion
- **Tâches** :
  - [ ] Créer un script `scripts/check_infra.py` qui :
    - Teste la connexion à l'instance Qdrant locale.
    - Vérifie si la collection `jumia_products` existe (sinon la créer).
    - Teste l'accessibilité de l'API OpenAI.
    - Teste l'accessibilité d'Evolution API.

## ✅ DEFINITION OF DONE (DoD)
- Evolution API est opérationnel via Docker.
- La collection `jumia_products` est initialisée dans le Qdrant existant.
- Le script `check_infra.py` valide tous les accès techniques.
