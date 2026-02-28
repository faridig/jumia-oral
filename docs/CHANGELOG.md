# 📜 CHANGELOG

## [0.4.0] - 2026-02-28
### Added
- **Architecture Multi-Catégorie v2 (PBI-120)** :
  - Nouveau schéma Pydantic `CategoryAgnosticProduct` séparant les métadonnées universelles des spécifications techniques dynamiques.
  - Normalisation intelligente des unités (Go/GB, ml, To/TB) via instructions LLM renforcées.
  - Analyse de sentiment multidimensionnelle (Performance, Design, Autonomie, Prix) avec scores 0-10 et rationales.
  - Intégration du `value_for_money_score` et recalibrage du `trust_score`.
  - Système de rangement automatique des fiches Markdown par dossiers catégories.
- **Simplification Logistique** : Retrait de la complexité PBI-130 (frais de livraison) pour garantir la stabilité du scraper multi-catégorie.

## 💡 LEÇONS APPRISES
### Sprint 2 : Réforme & Simplification
- **Arbitrage Complexité/Valeur** : L'extraction dynamique des frais de livraison via interactions JS multiples s'est avérée trop instable par rapport à la valeur ajoutée immédiate. La simplification a permis de se concentrer sur la robustesse des données produits.
- **Normalisation LLM** : `gpt-4o-mini` est excellent pour la normalisation d'unités techniques si le schéma Pydantic est bien typé (`Dict[str, Any]`).
- **Structure RAG-Ready** : L'utilisation de dossiers par catégorie dans `data/raw/markdown/` facilite grandement le futur filtrage par métadonnées dans la base vectorielle.
- **Lazy-Loading des Images** : L'expansion dynamique des avis peut masquer ou décharger la galerie d'images. L'ajout d'un scroll préventif et d'un retour au sommet (`window.scrollTo(0,0)`) est crucial pour garantir que le LLM "voit" les médias avant l'extraction.

## [0.3.0] - 2026-02-27
### Added
- **Scraper v1.1 (PBI-110)** :
  - Support multi-images (galerie) dans le schéma et le rendu Markdown.
  - Extraction des informations détaillées du vendeur (score, vitesse, abonnés).
  - Expansion dynamique des avis clients via injection JavaScript avant extraction.
  - Augmentation de la limite de traitement à 10 produits par batch.
  - Suite de tests unitaires pour valider la robustesse du nouveau schéma.

## 💡 LEÇONS APPRISES
### Sprint 1 : Optimisation du Scraper
- **Pollution Visuelle LLM** : L'extraction d'images peut être parasitée par les éléments d'UI (icônes de chat, logos). *Action future* : Prétraiter les sélecteurs d'images ou renforcer l'instruction LLM "exclude UI icons".
- **Dynamisme JS** : L'utilisation de `js_code` pour cliquer sur "Voir plus" dans les avis augmente significativement la qualité du `review_summary`, mais nécessite une gestion fine des timeouts pour éviter les `Execution context destroyed`.
- **Informations Vendeur** : Ces données sont cruciales pour le `trust_score` futur. Leur extraction via LLM est stable mais dépend fortement de la visibilité du bloc à l'écran.

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
