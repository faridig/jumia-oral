# 📜 CHANGELOG

## [Unreleased]

## [0.2.0] - 2026-02-26
### Added
- **Sprint 1 : Scraping Intelligent (PBI-101/102/103)** :
  - Crawler performant avec pagination (10 pages, ~420 URLs uniques).
  - Scraping LLM-powered avec `Crawl4AI` et `gpt-4o-mini`.
  - Calcul du `trust_score` basé sur les notes et le volume d'avis.
  - Génération automatique de fiches produits au format Markdown avec Frontmatter YAML.

## 💡 LEÇONS APPRISES
### Sprint 1 : Scraping & Extraction
- **Crawl4AI vs Pagination** : L'utilisation de `JsonCssExtractionStrategy` est extrêmement efficace pour la collecte d'URLs en masse avant de passer à l'extraction lourde (LLM).
- **Logique de Trust Score** : Le calcul `(Note * 0.7) + (log10(Avis) * 0.3)` permet de bien différencier un produit avec une note parfaite mais un seul avis d'un produit très populaire avec une note légèrement inférieure.
- **Gestion du Cache** : Le mode `CacheMode.BYPASS` est nécessaire sur Jumia pour éviter les données périmées lors des tests fréquents.
- **Stabilité LLM** : `gpt-4o-mini` offre un excellent rapport qualité/prix pour l'extraction de schémas structurés complexes, mais il est préférable de traiter les produits en petits batchs pour éviter les timeouts ou limites de quota.

## [0.2.0] - 2026-02-26
### Added
- **Sprint 0 Terminé** : Infrastructure validée (Evolution API + Qdrant local).
- Arborescence du projet créée et environnement Python prêt.
- Script de validation technique `check_infra.py` opérationnel.

## [0.1.0] - 2026-02-26
### Added
- Phase de Brainstorming terminée avec le client.
- **WhatsApp Integration** : Choix de Evolution API (Open Source).
- **Extraction intelligente** : Passage à `LLMExtractionStrategy` (Crawl4AI + GPT-4o-mini).
- **Personnalité** : Définition du ton "Commercial/Amical Marocain" (Darija).
- **Features RAG** : Recherche hybride, comparaison de produits, score de confiance.
- **Limite MVP** : Scraping limité aux 10 premières pages par catégorie.
- **Infrastructure** : Setup Docker pour Evolution API et script de validation `check_infra.py`.
