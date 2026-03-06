# 📜 CHANGELOG

## [1.2.0] - 2026-03-06
### Added
- **Gold Dataset Evaluation (PBI-1200)** : Mise en place d'un jeu de données de référence (26 cas) pour la validation scientifique du bot.
- **Automatisation de la Génération** : Script `scripts/generate_test_data.py` utilisant GPT-4o-mini pour transformer les fiches techniques en couples Question/Réponse réalistes.
- **Tests de Structure Dataset** : Suite de tests `tests/test_pbi_1200.py` garantissant l'intégrité et la complétude du dataset de vérité.

## [1.1.0] - 2026-03-05
### Added
- **Le Compagnon Notebook (PBI-2000)** : Pivot majeur vers un moteur de recommandation pur sémantique et intentionnel.
- **Neutralité Algorithmique** : Retrait total des scores VFM et Trust Score pour éliminer tout biais artificiel dans les recommandations.
- **Dual Proposal Standard** : Contrainte de réponse présentant systématiquement deux options comparables avec liens Jumia cliquables.
- **Intelligence d'Usage** : Capacité de traduire des besoins métiers (Gaming, Études, Montage) en contraintes techniques CPU/RAM/GPU.
- **Reset Qdrant & Purge MD** : Réinitialisation complète de la base de données et suppression des anciens fichiers pour garantir l'intégrité des 30 produits Notebooks ingérés.
- **Full-Context Node** : Stratégie d'ingestion "1 produit = 1 chunk" garantissant l'accès complet au descriptif technique pour le LLM.
- **Épuration Qualitative** : Nettoyage de la Sentiment Analysis pour ne conserver que le rationale textuel (expertise) et supprimer les notes numériques.

## 💡 LEÇONS APPRISES
### Sprint 11 : Génération du Gold Dataset (Vérité Terrain)
- **Maîtrise du Scripting sur-mesure** : Préférer un script Python personnalisé aux générateurs "boîte noire" (LlamaIndex/DeepEval) permet un contrôle fin sur l'extraction des specs critiques (RAM, CPU) et garantit que le dataset reflète exactement les données réelles du catalogue.
- **Qualité vs Quantité** : Traiter l'intégralité du catalogue Notebook (26 produits) offre une couverture de test exhaustive. Chaque fiche produit devient un cas de test unique, ce qui est plus robuste qu'une génération purement aléatoire.
- **Structure JSON stricte** : L'utilisation du `response_format={"type": "json_object"}` avec OpenAI est indispensable pour garantir que le dataset produit soit immédiatement exploitable par les scripts d'évaluation automatisés sans erreur de parsing.

### Sprint 10 : Compagnon Notebook & Pureté Technique
- **Efficacité de la contrainte "Top 2"** : Limiter le choix à deux options force le moteur RAG à être plus sélectif et précis, évitant ainsi la surcharge cognitive pour l'utilisateur. La justification technique devient alors le coeur de la valeur ajoutée.
- **Suppression des Biais Business** : Le retrait des scores numériques (VFM/Trust) simplifie le modèle de données et renforce la crédibilité de l'expert, qui s'appuie désormais uniquement sur des faits techniques (CPU, RAM, GPU) et des justifications sémantiques.
- **Intégrité par le Full-Context Chunking** : L'approche "un produit = un node" est la seule garantie contre la fragmentation des informations techniques. En évitant le découpage arbitraire, on s'assure que le LLM a toujours accès à la fiche complète lors de la synthèse.
- **Cartographie des Intentions** : Le passage d'une recherche par mots-clés à un mappage par intentions d'usage (Gaming, Montage, Études) permet de traduire des besoins flous en contraintes matérielles rigides, augmentant drastiquement la pertinence de l'Auto-Retriever.

### Sprint 9 : Pivot PC Portables & Nettoyage
- **Pivot Catégoriel & Performance** : Le passage à une spécialisation PC Portables réduit drastiquement le bruit sémantique. Le nettoyage de l'arborescence (`data/raw/markdown/notebooks`) permet d'accélérer l'indexation et la précision des réponses.
- **Auto-Retriever & Métadonnées Techniques** : L'ajout de champs techniques (CPU, RAM, SSD) dans les métadonnées de l'Auto-Retriever est crucial pour les produits technologiques. Cela permet des filtres précis (ex: "8Go de RAM") que la recherche vectorielle seule pourrait rater.
- **Vérification de Propreté (Anti-Pollution)** : L'automatisation du nettoyage des données (`ls -R`) est une étape de validation indispensable pour éviter que d'anciens fichiers (smartphones, beauté) ne polluent les recommandations d'une nouvelle spécialité.
- **Compatibilité Client/Serveur Qdrant** : Les warnings de version entre le client Python et le serveur Qdrant (1.17 vs 1.10) ne sont pas bloquants mais soulignent l'importance de la synchronisation des images Docker en production pour éviter des comportements instables.

### Sprint 8 : WhatsApp Live & Onboarding
- **Exposition Local (Tunneling)** : L'utilisation d'un tunnel (ex: Ngrok) est indispensable en phase de développement pour recevoir les webhooks. Une URL statique stable est recommandée pour la persistance de la session WhatsApp.
- **BackgroundTasks vs Timeout** : Evolution API renvoie des "retries" si le webhook ne répond pas en moins de 5-10 secondes. Le pattern `BackgroundTasks` de FastAPI est critique ici : répondre `200 OK` d'abord, réfléchir avec le RAG ensuite.
- **Réception Multimédia** : Les webhooks `MESSAGES_UPSERT` de Evolution API contiennent un champ `messageType`. Il faut impérativement isoler la logique de texte de celle des médias (images/vidéos) dès la réception pour éviter les crashs de parsing.

### Sprint 7 : WhatsApp Gateway & Comparison Engine
- **Asynchronisme des Webhooks** : L'utilisation de `BackgroundTasks` dans FastAPI est indispensable pour répondre immédiatement au serveur Evolution API (évite les retries de message) tout en laissant le temps au RAG de générer une réponse complexe.
- **Intention de Comparaison** : Une détection basée sur des mots-clés bilingues (Fr/Darija) couplée à un prompt de synthèse dédié permet de transformer une recherche sémantique en un véritable outil d'aide à la décision structuré (Tableau Markdown + Verdict Darija).
- **Richesse Multimédia** : L'extraction automatique des URLs d'images depuis les métadonnées des produits permet de fournir un support visuel immédiat sur WhatsApp, renforçant la confiance de l'utilisateur.

### Sprint 7 : OpenRTK Plugin System
- **Intégration Transparente via Proxy** : L'utilisation de `rtk` comme proxy pour Git permet d'injecter une couche d'intelligence (emoji, résumé de tokens) sans modifier les binaires originaux. L'icône 📌 sert de signature visuelle pour confirmer que la couche d'optimisation est active.
- **Rigueur des Tests Unitaires** : Maintenir un taux de succès de 100% sur la suite de tests (56/56) est crucial avant toute modification du PATH système, car toute régression bloquerait le flux de travail de l'agent.
- **Pollution Visuelle CLI** : Un affichage compact (6-10 lignes pour un status complexe) réduit drastiquement la consommation de tokens de contexte et améliore la lisibilité pour l'LLM.
- **Hygiène du dépôt (Dotfiles)** : L'exclusion stricte des dossiers de configuration locale (comme `.opencode/`) via `.gitignore` et le nettoyage de l'index Git est impératif pour éviter la fuite de configurations spécifiques à l'environnement de dev et maintenir un dépôt propre.

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
