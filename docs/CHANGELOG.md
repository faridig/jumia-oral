# 📜 CHANGELOG

## [0.6.3] - 2026-03-03
### Added
- **Intégration OpenRTK (Plugin System)** : Déploiement du plugin de filtrage intelligent pour `rtk`. Ce plugin intercepte les commandes Git (notamment `git status`) pour fournir un affichage ultra-compact avec l'icône 📌 et des indicateurs visuels (📝, ❓).
- **Audit de Performance CLI** : Validation de la suite de tests (56 tests passés) et vérification du PATH pour l'outil `rtk`.

## [0.6.2] - 2026-03-03
### Added
- **Onboarding Localisation (PBI-310)** : Dialogue interactif en Darija pour identifier la ville de l'utilisateur et persistance de la session via `SimpleChatStore`.
- **Logiciel d'Expertise Isolé (PBI-502)** : Nouveau module `ExpertAdvisor` pour injecter des conseils professionnels (Dermatologue, Tech Analyst, etc.) basés sur la catégorie produit.

## [0.6.1] - 2026-03-01
### Added
- **Hard-Filtering de Pertinence (PBI-404)** : Instauration d'un seuil de similarité strict (0.8) pour éliminer les faux positifs sémantiques avant le re-ranking.

## [0.6.0] - 2026-03-01
### Added
- **Ré-optimisation du Re-ranking (PBI-401)** : Ajustement de la pondération (60% Sémantique / 40% Business) pour garantir la pertinence des résultats.
- **Transparence de Confiance (PBI-402)** : Mention systématique en Darija ("ba9i madiyoroch fih l-avis") pour les produits sans avis clients.
- **Affinage de l'Auto-Retriever (PBI-403)** : Optimisation des filtres métadonnées pour éviter l'over-filtering sur les requêtes simples.

## 💡 LEÇONS APPRISES
### Sprint 7 : WhatsApp Gateway & Comparison Engine
- **Asynchronisme des Webhooks** : L'utilisation de `BackgroundTasks` dans FastAPI est indispensable pour répondre immédiatement au serveur Evolution API (évite les retries de message) tout en laissant le temps au RAG de générer une réponse complexe.
- **Intention de Comparaison** : Une détection basée sur des mots-clés bilingues (Fr/Darija) couplée à un prompt de synthèse dédié permet de transformer une recherche sémantique en un véritable outil d'aide à la décision structuré (Tableau Markdown + Verdict Darija).
- **Richesse Multimédia** : L'extraction automatique des URLs d'images depuis les métadonnées des produits permet de fournir un support visuel immédiat sur WhatsApp, renforçant la confiance de l'utilisateur.

### Sprint 7 : OpenRTK Plugin System
- **Intégration Transparente via Proxy** : L'utilisation de `rtk` comme proxy pour Git permet d'injecter une couche d'intelligence (emoji, résumé de tokens) sans modifier les binaires originaux. L'icône 📌 sert de signature visuelle pour confirmer que la couche d'optimisation est active.
- **Rigueur des Tests Unitaires** : Maintenir un taux de succès de 100% sur la suite de tests (56/56) est crucial avant toute modification du PATH système, car toute régression bloquerait le flux de travail de l'agent.
- **Pollution Visuelle CLI** : Un affichage compact (6-10 lignes pour un status complexe) réduit drastiquement la consommation de tokens de contexte et améliore la lisibilité pour l'LLM.

### Sprint 6 : Location Onboarding & Expert Insights
- **Isolation de la Logique d'Expertise** : Séparer le moteur de recommandation de la logique de conseil pur (`ExpertAdvisor`) permet de changer de persona ou de style sans impacter la recherche vectorielle.
- **Gestion Hybride des Sessions** : L'utilisation détournée de `SimpleChatStore` pour stocker des métadonnées profil (localisation) simplifie l'architecture tout en assurant la persistance.
- **Onboarding par le Dialogue** : L'extraction de la ville via le dialogue direct est plus naturelle en Darija que des formulaires rigides. Un fallback sur un message clair est nécessaire si l'utilisateur ne répond pas directement.

### Sprint 5 : Qualité & Pertinence
- **Insuffisance des seuils bas** : Un seuil de similarité de 0.6 (souvent recommandé par défaut) laisse passer des produits très éloignés (ex: Cartouches d'encre vs Crèmes). Un seuil de 0.8 est nécessaire pour garantir une étanchéité catégorielle totale.
- **Régressions dans les Tests** : L'introduction d'un filtrage strict peut invalider des tests existants utilisant des données factices à faible score. Il est crucial d'ajuster les jeux de tests pour franchir les nouveaux seuils.
- **Vigilance Sales Compliance** : La recommandation d'un assistant RAG peut involontairement citer des concurrents si le prompt n'est pas verrouillé. Une instruction spécifique 'Sales Compliance' est indispensable pour protéger l'écosystème commercial.

### Sprint 4 : Re-optimisation & Transparence
- **Pondération Sémantique vs Business** : Un ratio de 60/40 semble être le point d equilibrium idéal pour éviter les produits hors-sujet tout en mettant en avant les bonnes affaires.
- **Transparence Trust Score** : L injection directe du score de confiance dans le prompt système, couplée à une consigne Darija stricte, humanise l assistant et renforce la crédibilité de la plateforme.
- **Résilience Auto-Retriever** : Toujours prévoir un fallback sur la recherche vectorielle classique car l extraction de filtres structurés par le LLM peut échouer sur des requêtes trop familières ou ambiguës.

---

## [0.5.0] - 2026-02-28
### Added
- **Moteur RAG Avancé (PBI-210)** :
  - Implémentation du **Multi-Query expansion** : Traduction dynamique Darija -> Français technique pour optimiser le matching vectoriel.
  - Intégration de l'**Auto-Retriever LlamaIndex** : Extraction automatique de filtres métadonnées (prix, marque, catégorie) depuis le langage naturel.
- **Personnalité & Intelligence Commerciale (PBI-301)** :
  - Tone of Voice "Jumia Oral" : Réponses bilingues (Darija/Français) avec expressions locales (Mrehba, Besseha).
  - Logique de **Re-ranking multi-critères** : Pondération dynamique combinant pertinence sémantique (40%), Trust Score (24%) et Value for Money (36%).

## [0.4.0] - 2026-02-28
### Added
- **Architecture Multi-Catégorie v2 (PBI-120)** :
  - Nouveau schéma Pydantic `CategoryAgnosticProduct` séparant les métadonnées universelles des spécifications techniques dynamiques.
  - Analyse de sentiment multidimensionnelle (Performance, Design, Autonomie, Prix).

## [0.3.0] - 2026-02-27
### Added
- **Scraper v1.1 (PBI-110)** :
  - Support multi-images et informations détaillées du vendeur.
  - Expansion dynamique des avis clients via injection JavaScript.

## [0.2.0] - 2026-02-26
### Added
- **Sprint 1 : Scraping Intelligent (PBI-101)** :
  - Crawler performant (10 pages, ~420 URLs).
  - Calcul du `trust_score` et génération de fiches Markdown.

## [0.1.0] - 2026-02-26
### Added
- **Infrastructure Initialisée** : Setup Evolution API & Qdrant local.
- **Vision Produit** : Ton Darija & Personal Shopper RAG.
