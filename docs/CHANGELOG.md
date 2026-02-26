# 📜 CHANGELOG

## [Unreleased]

### 💡 LEÇONS APPRISES (Sprint 0)
- **Configuration Docker** : L'Evolution API nécessite obligatoirement une base de données PostgreSQL externe (ou dans le même compose) pour persister les sessions WhatsApp. L'utilisation de `DATABASE_PROVIDER=postgresql` est cruciale.
- **Gestion Qdrant** : Dans un environnement où Qdrant est déjà mutualisé, il est préférable de ne pas l'inclure dans le `docker-compose.yml` local pour éviter les conflits de ports (6333/6343), mais de déléguer la vérification de la collection au script d'initialisation.
- **Dépendances Python** : Attention aux versions non-épinglées dans `requirements.txt` qui peuvent générer des `RequestsDependencyWarning` liés à `urllib3`. Un futur passage à `pip-compile` ou `poetry` est recommandé.

## [0.1.0] - 2026-02-26
### Added
- Phase de Brainstorming terminée avec le client.
- **WhatsApp Integration** : Choix de Evolution API (Open Source).
- **Extraction intelligente** : Passage à `LLMExtractionStrategy` (Crawl4AI + GPT-4o-mini).
- **Personnalité** : Définition du ton "Commercial/Amical Marocain" (Darija).
- **Features RAG** : Recherche hybride, comparaison de produits, score de confiance.
- **Limite MVP** : Scraping limité aux 10 premières pages par catégorie.
- **Infrastructure** : Setup Docker pour Evolution API et script de validation `check_infra.py`.
