# 📜 CHANGELOG

## [1.8.0] - 2026-03-26
### Added
- **Expérience Multimodale & Voice (PBI-1701)** :
  - Intégration de **OpenAI TTS (tts-1)** pour la synthèse vocale haute performance en format **.opus**.
  - Séquençage intelligent des messages sur WhatsApp : **Image -> Texte -> Audio** pour une UX premium.
  - Double flux de sortie RAG : Texte riche avec emojis/liens pour [WHATSAPP] et texte fluide phonétique pour [TTS].
  - Optimisation de la transmission audio via **Base64** pour éliminer la latence du stockage disque.

### Sprint 17 : Sawt El Moustahlik (Multimodalité & Orchestration)
- **Script Arabe pour la Prosodie (TTS)** : L'utilisation de l'alphabet latin (Arabizi) pour la synthèse vocale produit souvent un accent "robotique" ou étranger. Forcer le LLM à générer le flux `[TTS]` en **script arabe** (tout en restant en Darija) permet au moteur OpenAI TTS de mieux interpréter la phonétique et de délivrer un accent marocain beaucoup plus authentique et chaleureux.
- **Supériorité de l'Audio Natif (GPT-4o)** : L'audit dynamique a révélé que le moteur `tts-1` classique conserve des biais égyptiens (prononciation en "G"). Le passage au modèle `gpt-4o-audio-preview` avec une voix `onyx` et des instructions de style "Casa Street" permet d'obtenir un accent marocain d'élite, sec et percutant, en éliminant les intonations tunisiennes ou fusha.
- **Séquençage et Engagement UX** : L'ordre d'envoi des messages (Image d'abord, puis texte, puis voix) est crucial. L'image capte l'attention, le texte donne les détails actionnables (liens), et la voix humanise la relation. Inverser cet ordre brise le flux de lecture naturel sur mobile.
- **Optimisation de la Latence (Base64 vs File)** : Passer par un encodage Base64 pour l'envoi de médias via l'API Evolution réduit drastiquement les IO disque et les risques de fichiers temporaires orphelins, tout en accélérant la réponse perçue par l'utilisateur.
- **Double Persona LLM (Prosodie vs Structure)** : Un seul texte ne peut pas servir à la fois pour la lecture (besoin de gras, emojis, liens) et pour l'écoute (besoin de fluidité, pas de caractères spéciaux). La séparation via balises `[WHATSAPP]` / `[TTS]` dans le prompt système est la méthode la plus robuste pour garantir une qualité optimale sur les deux canaux simultanément.
- **Validation Réelle des APIs Tierces** : Les mocks peuvent masquer des erreurs de configuration fatales (comme des noms de voix non supportés). L'audit dynamique avec un appel réel à l'API (OpenAI TTS) a permis d'identifier une erreur 400 que les tests unitaires mockés n'auraient jamais détectée. Toujours valider les paramètres "énumérés" (voix, modèles) par un test d'intégration réel.
- **Choix du Moteur TTS** : Bien que `gpt-4o-mini-tts` soit le moteur interne, spécifier `model="tts-1"` dans l'API OpenAI garantit l'accès au moteur optimisé pour la vitesse, essentiel pour une interaction quasi-instantanée (<2s) sur WhatsApp.

## [1.7.0] - 2026-03-25
### Added
- **Whisper et Darija Native (PBI-1103)** :
  - Intégration de **OpenAI Whisper** pour la transcription des messages vocaux WhatsApp en Darija marocain.
  - Optimisation du prompt Whisper avec un contexte technique (PC Jumia, madi, tayra) pour une précision accrue.
  - Passage au modèle **GPT-4o** pour une "Pensée Native" en Darija, utilisant un glossaire local validé.
  - Mise en place d'un onboarding vocal invitant explicitement les utilisateurs à parler au bot.
- **Maintenance Infra (PBI-1601)** : Alignement du client Qdrant avec la version serveur (1.10.0).

### Sprint 16 : Sawt El Bled (Interaction Vocale & Darija Native)
- **Whisper et Contexte Dialectal** : L'utilisation du paramètre `prompt` de Whisper est indispensable pour guider la transcription vers un dialecte spécifique comme le Darija. Inclure des termes techniques du catalogue dans ce prompt réduit drastiquement les erreurs de transcription phonétique.
- **Robustesse du Monitoring (Phoenix)** : Ne jamais laisser l'infrastructure de monitoring (tracing/OTLP) bloquer le démarrage de l'application métier. L'encapsulation de l'initialisation de Phoenix dans un bloc `try/except` avec une dégradation gracieuse (mode sans tracing) est une nécessité pour la haute disponibilité.
- **Mocks et Paramètres API** : Lors des tests unitaires sur des APIs tierces (OpenAI), il est crucial de vérifier non seulement les données envoyées, mais aussi le nom exact des paramètres attendus par la librairie cliente (ex: `prompt`). Une erreur de nommage dans un mock peut masquer un bug réel ou invalider un test valide.
- **Pensée Native (GPT-4o)** : Le passage à GPT-4o couplé à une instruction de "Pensée Native en Darija" (plutôt que de simple traduction) transforme radicalement l'expérience utilisateur. L'utilisation d'expressions idiomatiques (`mkhyr`, `tayra`, `madi`) renforce l'identité de marque locale "Jumia Oral".

## [1.6.0] - 2026-03-25
### Added
- **Intelligence d'Intention & Stabilité (PBI-1102)** :
  - Mise en œuvre de l'**Auto-Retriever** structuré pour transformer des besoins métiers (Gaming, Études, Montage) en filtres techniques matériels (RAM, CPU).
  - Correction majeure de stabilité sur le typage `RESPONSE_TYPE` de LlamaIndex, garantissant l'absence d'erreurs de type lors du streaming des réponses.
  - Configuration rigoureuse du schéma de métadonnées (`AttributeInfo`) pour une précision accrue des filtres de recherche.

## [1.5.0] - 2026-03-16
### Added
- **Mémoire Contextuelle (PBI-1001)** : Transition vers `ContextChatEngine` et `SimpleChatStore`. Le bot conserve désormais l'historique des échanges par numéro WhatsApp, permettant des questions de suivi naturelles sur les produits cités.
- **Expansion du Catalogue (PBI-902b)** : Scraping et indexation de 5 pages de la catégorie Notebooks (~200 produits). Extraction enrichie des métadonnées techniques (CPU, RAM, SSD) via LLM.
- **Naturalité Darija (PBI-1101)** : Implémentation d'un glossaire technique "Darija-Tech" dans le System Prompt pour aligner les recommandations avec le langage familier des utilisateurs marocains.

## [1.4.0] - 2026-03-12
### Added
- **Observabilité & Tracing (PBI-1306)** : Intégration de **Arize Phoenix**. Tracing complet du flux RAG (Retriever -> Synthesis) pour monitorer la latence et les coûts de tokens en temps réel.
- **Audit d'Intégrité Technique (PBI-1301/1303)** : Mise en place de **DeepEval** et **Confident AI**. Évaluation scientifique automatisée basée sur le `gold_dataset.json` avec mesure des métriques : Faithfulness, Contextual Recall, et Answer Relevancy.

### Removed
- **Nettoyage Expert Advisor (PBI-1002)** : Suppression définitive de la dépendance à Context7/Expert Advisor. Le moteur RAG se concentre désormais exclusivement sur les données natives Jumia pour éviter tout bruit externe.

## [1.3.0] - 2026-03-08
### Added
- **Alignement Vision "Notebook Companion" (PBI-1201)** : Refonte totale du README pour refléter la spécialisation exclusive sur les PC Portables et la suppression des biais business.
- **Hygiène du Code & Démo (PBI-1202)** : Mise à jour de `src/main.py` pour refléter le flux conversationnel actuel, débarrassé des étapes d'onboarding géographiques.

### Changed
- **Retrait de la Localisation (PBI-1006)** : Suppression définitive de la gestion des villes et de la logistique dans le moteur de session et le prompt système pour un focus produit maximal.

## 💡 LEÇONS APPRISES
### Sprint 17 : Sawt El Moustahlik (Multimodalité & Orchestration)
- **Récupération du Persona (Recovery)** : Lors d'une migration technique majeure (ex: passage à l'Audio Natif GPT-4o), le style de réponse peut dériver vers une concision excessive ou une perte de politesse. La réinjection explicite de salutations marocaines (`Mrehba`, `Salam`) et l'usage de vocabulaire de proximité (`khouya`, `sahbi`) sont indispensables pour maintenir l'ADN "chaleureux" de Jumia Oral.
- **Structure Fact-First** : Pour éviter que le style (Darija de rue) ne prenne le pas sur la précision, imposer une structure "Fact-First" dans le prompt (modèle et specs dès la première phrase) garantit que l'utilisateur reçoit d'abord la valeur technique avant l'enrobage social.
- **Double Persona LLM (Prosodie vs Structure)** : Un seul texte ne peut pas servir à la fois pour la lecture (besoin de gras, emojis, liens) et pour l'écoute (besoin de fluidité, pas de caractères spéciaux). La séparation via balises `[WHATSAPP]` / `[TTS]` dans le prompt système est la méthode la plus robuste pour garantir une qualité optimale sur les deux canaux simultanément.

### Sprint 15 : Intelligence Stable
- **Précision du Typage dans LlamaIndex** : L'utilisation de types `Union` explicites pour les réponses (`Response | StreamingResponse`) est impérative pour maintenir la robustesse du moteur RAG lors de l'utilisation de `QueryEngine` ou `ChatEngine`.
- **L'Auto-Retriever comme Pont Sémantique-Technique** : L'extraction de métadonnées ne suffit pas ; il faut un "Intelligence Mapping" robuste dans le prompt pour que le LLM sache qu'un "étudiant" a besoin de portabilité et d'autonomie, alors qu'un "gamer" a besoin d'un GPU et de RAM.

### Sprint 12 : Hygiène & Alignement
- **Importance de la Cohérence Documentaire** : Un README obsolète peut freiner l'adoption du projet ou induire les futurs développeurs en erreur. Aligner la documentation dès qu'un pivot technique est stabilisé est crucial.
- **Simplification du Flux (Less is More)** : En retirant la localisation, on réduit les points de friction lors de l'onboarding utilisateur sur WhatsApp, permettant d'entrer directement dans le coeur de la valeur : le conseil expert.
- **Script de Démo comme Documentation Vivante** : Maintenir `src/main.py` à jour permet de tester instantanément la chaîne RAG complète sans dépendre de l'infrastructure WhatsApp complexe.

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
