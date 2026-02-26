# 🏃 SPRINT PLAN - SPRINT 0 (INFRASTRUCTURE)

## 🎯 OBJECTIF
Mettre en place l'environnement de développement, l'infrastructure Docker et valider la chaîne de connexion technique.

## 📋 TÂCHES À RÉALISER

### [PBI-000] Initialisation de l'Espace de Travail
- **Tâches** :
  - [ ] Créer l'arborescence complète : `src/`, `scripts/`, `data/raw/markdown/`, `docs/`, `logs/`.
  - [ ] Créer le fichier `requirements.txt` (Crawl4ai, LlamaIndex, Qdrant-client, FastAPI, python-dotenv).
  - [ ] Créer le fichier `.env.example` incluant : `OPENAI_API_KEY`, `QDRANT_URL`, `EVOLUTION_API_KEY`.

### [PBI-001] Infrastructure Docker
- **Tâches** :
  - [ ] Créer un fichier `docker-compose.yml` incluant :
    - Service `qdrant` (image: qdrant/qdrant).
    - Service `evolution-api` (image: atendimento/evolution-api).
  - [ ] Lancer les containers et vérifier l'accessibilité des ports (6333 et 8080).

### [PBI-002] Walking Skeleton & Validation
- **Tâches** :
  - [ ] Créer un script `scripts/check_infra.py` qui :
    - Charge les variables d'environnement.
    - Teste la connexion à l'instance Qdrant.
    - Teste un appel minimal à l'API OpenAI (ChatCompletion).
  - [ ] Créer un fichier `src/main.py` vide servant de point d'entrée futur.

## ✅ DEFINITION OF DONE (DoD)
- L'infrastructure Docker est "Up and Running".
- Le script `check_infra.py` s'exécute sans erreur.
- Le fichier `README.md` est à jour avec les instructions d'installation.
