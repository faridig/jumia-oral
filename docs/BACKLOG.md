# 🚀 BACKLOG - JUMIA RAG PROJECT

## ⚙️ CONFIGURATION TECHNIQUE
- **Langage** : Python 3.10+
- **Framework Scraping** : Crawl4AI avec **LLMExtractionStrategy** (GPT-4o-mini).
- **Orchestration RAG** : LlamaIndex avec **Hybrid Search** (Dense + Sparse).
- **Vector Database** : Qdrant (Utilisation de l'instance locale existante).
- **Isolation des données** : Collection dédiée `jumia_products`.
- **WhatsApp Gateway** : Evolution API (Open Source Baileys-based).
- **Mémoire Conversationnelle** : SimpleChatStore (Persistance JSON par numéro).
- **Format de sortie** : Markdown avec Frontmatter YAML.
- **Stratégie de Chunking** : **Full-Context Node** (1 produit = 1 chunk unique) pour préserver l'intégrité technique.
- **Visibilité LLM** : 100% des métadonnées (Prix, URL, Specs) transmises au modèle.

## 🏛️ JOURNAL DES DÉCISIONS
1. **[2026-02-26] Choix de Crawl4AI & LLM Extraction** : Pour garantir l'extraction des avis profonds et des specs techniques sans maintenance de sélecteurs.
...
17. **[2026-03-05] Suppression de la Localisation & Focus Produit** : Décision de supprimer toute gestion de la localisation utilisateur (villes, livraison locale). L'agent est désormais strictement dédié à la recommandation produit technique.
18. **[2026-03-05] Support Vocal & Darija Natif** : Décision d'integrer le support des messages vocaux (STT). Le système doit être capable de comprendre le Darija parlé (via Whisper ou équivalent performant) et de répondre avec une structure grammaticale Darija authentique, dépassant le simple mélange de mots.
19. **[2026-03-05] Recherche par Intention d'Usage** : Transition d'une recherche par mots-clés vers une compréhension des besoins métiers (Gaming, Montage, Études) pour filtrer automatiquement les specs techniques requises.
20. **[2026-03-05] Stratégie "Full-Context Chunking"** : Abandon du découpage par phrases ou sections. Chaque fiche Notebook Jumia (< 2000 tokens) sera ingérée comme un **Node unique**. Cela garantit que le LLM a accès à toutes les specs techniques et à l'URL Jumia sans répétition inutile ou perte de lien entre les métadonnées et le descriptif.
21. **[2026-03-05] Épuration de la Sentiment Analysis (Pure Rationale)** : Pour être cohérent avec le retrait du VFM et du Trust Score, les **notes numériques** (scores 0-10) et l'axe **"Value"** sont supprimés de l'analyse de sentiment. On ne conserve que le **Rationale** (texte descriptif) pour les axes techniques (Performance, Build Quality, Display) afin de nourrir le RAG en arguments qualitatifs neutres.
22. **[2026-03-06] Choix Technologique Gold Dataset (PBI-1200)** : Pour favoriser la montée en compétence technique et la maîtrise du style Darija, l'option **Script Python Sur-Mesure + OpenAI** est choisie à la place des outils natifs (LlamaIndex Generator) ou spécialisés (DeepEval). Cela permet un contrôle total sur l'extraction des specs critiques (RAM, CPU, Prix) et sur la langue de la question.

## 🧠 SYNCHRONISATION INTER-AGENTS (DANS LE BACKLOG)
1.  **Pour le REVIEWER** : Voir section DoD ci-dessous.
2.  **Pour le LEAD-DEV** : Voir le Journal des Décisions.
3.  **Pour l'UX & Présentation** : 
    - [Schéma d'Architecture & Parcours Client](PROJECT_ARCHITECTURE.md)
    - [Stratégie de Prompting](PROMPT_STRATEGY.md)

## ✅ DEFINITION OF DONE (DoD)
- Extraction : Données structurées validées par le schéma Pydantic (Enrichi Laptop).
- RAG : Capacité de comparaison entre 2 modèles de PC (ex: i5 vs i7).
- UX : Chatbot réactif sur WhatsApp avec gestion du contexte utilisateur.
- Sécurité : Variables d'environnement pour toutes les clés API.
- **Laptop Expertise** : Le bot doit être capable d'expliquer les différences techniques (RAM DDR4 vs DDR5, SSD NVMe) en Darija.
- **Sales Compliance** : Aucun nom de concurrent ou prix externe ne doit filtrer dans les réponses.
- **Pertinence Pure** : Seule la similarité sémantique et les caractéristiques techniques réelles (CPU, RAM, Prix) guident la recommandation.
- **Single Sniper Recommendation** : Chaque recommandation doit systématiquement présenter LA meilleure option trouvée, en justifiant pourquoi c'est le choix idéal pour l'utilisateur.
- **Sales Conversion Audio** : L'audio doit être persuasif, utiliser des adjectifs valorisants en Darija et pousser à l'action immédiate (clic sur le lien).

## 🎯 STRATÉGIE D'ÉVALUATION & QUALITÉ

### 🧪 LABO (AUDIT PRÉ-PROD) - The Shield
- **Source** : `tests/gold_dataset.json`.
- **Objectif** : Non-régression technique et intégrité des specs.
- **Fréquence** : À chaque commit (CI/CD via Pytest).
- **Métriques Critiques** :
    - **Faithfulness** : Zéro hallucination sur les specs Jumia.
    - **Answer Correctness** : Identité sémantique avec le corrigé "Gold".
    - **Contextual Recall** : Capacité à trouver les pépites du catalogue.

### 📡 TERRAIN (MONITORING LIVE) - The Cockpit
- **Source** : Logs réels (Evolution API / Phoenix).
- **Objectif** : Alignement avec le besoin client et authenticité Darija.
- **Fréquence** : Échantillonnage hebdomadaire (50 convs).
- **Métriques Critiques** :
    - **Answer Relevancy** : Utilité du conseil pour l'utilisateur.
    - **Contextual Precision** : Audit du Top 2 sur des requêtes réelles.
    - **G-Eval : Darija Tone** : Note sur le naturel et la culture marocaine.

### 🥋 STANDARDS "BLACK BELT" (SCÉNARIOS DE DIAGNOSTIC)
- **L'Honnête Inutile** : High Faithfulness / Low Relevancy. (Le bot ne ment pas mais ne sert à rien).
- **Le Chercheur Bruyant** : High Recall / Low Precision. (Le bot trouve le bon produit mais le noie dans le bruit).
- **Le Chanceux Halluciné** : Low Faithfulness / High Correctness. (Le bot a raison par chance mais ignore les données Jumia).
- **Le Sniper Aveugle** : Low Recall / High Precision. (Le bot est très précis mais ignore 90% des alternatives).

---

## 📋 BACKLOG GÉNÉRAL

### [PBI-1901] TECH : Vérification Temps-Réel (Stock/Lien)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : M
**User Story** : "En tant qu'utilisateur, je veux être sûr que le lien Jumia recommandé est toujours valide et le produit en stock."
**Critères d'Acceptation (Gherkin)** :
- [x] **Scenario 1 : Lien mort détecté**
  - **GIVEN** Le RAG sélectionne un produit dont l'URL renvoie un 404.
  - **WHEN** Le système effectue le check pre-flight.
  - **THEN** Le produit est ignoré et le suivant dans le top-k est sélectionné.

### [PBI-1902] PROMPT : Stratégie de Relance "Besoin d'aide ?"
**Status** : DONE ✅
**Priorité** : Medium | **Estimation** : S
**User Story** : "En tant que Personal Shopper, je veux relancer poliment l'utilisateur si la discussion est restée en suspens."
**Critères d'Acceptation** :
- [x] Création d'un prompt de relance chaleureux en Darija.
- [x] Logique de déclenchement (Optionnel pour ce sprint, focus sur le prompt).

### [PBI-1903] EVAL : Test de Robustesse "Adversarial Darija"
**Status** : DONE ✅
**Priorité** : High | **Estimation** : M
**User Story** : "En tant que PO, je veux m'assurer que le bot ne sort jamais de son rôle même s'il est provoqué."
**Critères d'Acceptation** :
- [x] Ajout de 10 cas de tests "provocations/insultes" dans `gold_dataset.json`.
- [x] Validation du maintien du Persona "Sales Professional" malgré le bruit.

### [PBI-1904] PROMPT : High-Conversion Sniper & Sales Audio
**Status** : DONE ✅
**Priorité** : CRITIQUE | **Estimation** : S
**User Story** : "En tant que vendeur Jumia, je veux que le bot ne propose qu'un seul produit avec un argumentaire vocal irrésistible."
**Critères d'Acceptation** :
- [x] **Moteur RAG** : Limitation à 1 seule recommandation par réponse.
- [x] **Flux [WHATSAPP]** : Focus sur l'unique lien.
- [x] **Flux [TTS]** : Ton persuasif ("Had l-bi si madi", "Mat-tfeltouch").

### [PBI-1801] TECH : Session TTL (Mémoire Éphémère & Hygiène)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : M
**User Story** : "En tant qu'utilisateur, je veux que le bot oublie nos anciennes discussions après une période d'inactivité (30 min), afin de repartir sur un besoin frais sans confusion."
**Critères d'Acceptation (Gherkin)** :
- [x] **Scenario 1 : Expiration de session**
  - **GIVEN** Une discussion active datant de plus de 30 minutes.
  - **WHEN** L'utilisateur envoie un nouveau message.
  - **THEN** Le `SimpleChatStore` vide l'historique précédent pour ce numéro.
- [x] **Scenario 2 : Maintien du Persona**
  - **GIVEN** Un reset de session.
  - **WHEN** Le bot répond.
  - **THEN** Il conserve son ton Darija et ses instructions système malgré l'oubli du contenu.

### [PBI-1802] TECH : Résolution Dette Technique (Type Error)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : S
**User Story** : "En tant que Lead-Dev, je veux corriger l'erreur de type sur `RESPONSE_TYPE` pour garantir la stabilité du moteur de chat."

### [PBI-1803] EVAL : Audit Qualité "Sawt Jumia" (Sprint 17 Logs)
**Status** : DONE ✅
**Priorité** : Medium | **Estimation** : S
**User Story** : "En tant que PO, je veux analyser les premiers logs réels du Sprint 17 pour vérifier si la prosodie Darija est bien acceptée par les utilisateurs."
**Critères d'Acceptation** :
- [x] **Scenario 1 : Analyse de pertinence**
  - **GIVEN** 20 logs de conversations réelles (Vocal/Multimodal).
  - **WHEN** Passés dans le framework DeepEval.
  - **THEN** Le score d'Answer Relevancy doit être > 0.7.

### [PBI-901] TECH : Purge & Reset (Clean Slate)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : XS
**User Story** : "En tant que Lead-Dev, je veux vider les données obsolètes pour garantir que mon moteur RAG ne recommande que des PC Portables."
**Critères d'Acceptation** :
- [x] Suppression physique des fichiers `.md` et `.csv` dans `data/`.
- [x] Suppression et re-création de la collection `jumia_products` dans Qdrant.

### [SPIKE-902] TEST : Extraction "Micro-Batch" (10 Produits)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : XS
**User Story** : "En tant que Chef d'Orchestre, je veux tester l'extraction LLM on 10 produits pour valider la structure des métadonnées PC sans gaspiller de tokens."
**Critères d'Acceptation** :
- [x] Limiter le scraping aux 10 premiers produits de Jumia Notebooks.
- [x] Générer un rapport JSON des métadonnées extraites (CPU, RAM, SSD, GPU, Écran).
- [x] Validation manuelle du résultat par le Chef d'Orchestre avant passage à l'échelle.

### [PBI-902b] SCRAPING : Extraction Totale "Notebooks" (5 Pages)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : M
**User Story** : "En tant que Personal Shopper, je veux extraire les fiches techniques des 5 premières pages de Jumia Notebooks après validation du Spike."
**Critères d'Acceptation** :
- [x] Crawling de `https://www.jumia.ma/notebooks/`.
- [x] Extraction LLM basée sur la structure validée au Spike.
- [x] Stockage structuré dans `data/`.

### [PBI-903] INGESTION : Indexation Vectorielle PC Portables
**Status** : DONE ✅
**Priorité** : High | **Estimation** : M
- [x] Ingestion des nouvelles données dans le moteur RAG.
- [x] Vérification de la recherche hybride sur des requêtes techniques (ex: "PC i7 16GB").

### [PBI-1001] TECH/UX : Mémoire Contextuelle de Recherche (Shopping Dialogue)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : M

**User Story** : "En tant que Personal Shopper, je veux que le bot se souvienne des produits précédemment cités, afin que l'utilisateur puisse poser des questions de suivi (ex: 'Et son autonomie ?') sans répétition fastidieuse."

**Dépendances** : PBI-210 (Moteur RAG)

**Critères d'Acceptation (Gherkin)** :
- [x] **Scenario 1 : Question de suivi sur un produit**
  - **GIVEN** L'utilisateur a déjà reçu une description du "MacBook Air M2".
  - **WHEN** L'utilisateur demande : "Et son autonomie ?".
  - **THEN** Le bot identifie que "son" se rapporte au MacBook Air M2 et répond via le RAG sur ce contexte précis.
- [x] **Scenario 2 : Transition vers ContextChatEngine**
  - **GIVEN** Le `src/rag_engine.py` utilise un `QueryEngine`.
  - **WHEN** On initialise le moteur RAG.
  - **THEN** Il doit exposer une interface `chat` (LlamaIndex ContextChatEngine) au lieu de `query`.
- [x] **Scenario 3 : Persistence de l'historique**
  - **GIVEN** Un utilisateur WhatsApp identifié par son numéro.
  - **WHEN** Plusieurs échanges ont lieu.
  - **THEN** Le `SimpleChatStore` doit sauvegarder et recharger l'historique pour maintenir la cohérence sur plusieurs jours.

### [PBI-1002] TECH : Nettoyage & Retrait Context7 (Expert Advisor)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : S
**User Story** : "En tant que Lead-Dev, je veux supprimer les appels à l'Expert Advisor (MCP) dans le moteur RAG pour me baser uniquement sur les descriptions Jumia."
**Critères d'Acceptation** :
- [x] Suppression de l'import et de l'usage de `expert_advisor` dans `src/rag_engine.py`.
- [x] Suppression physique du fichier `src/expert_advisor.py`.
- [x] Suppression de la logique de `expert_node` dans la synthèse de réponse.
- [x] Validation que les réponses LLM ne citent plus de sources externes.

### [PBI-1301] SETUP : Instrumentation DeepEval, Confident AI & LlamaIndex
**Status** : DONE ✅
**Priorité** : High | **Estimation** : S
**User Story** : "En tant que Lead-Dev, je veux intégrer le framework DeepEval et la plateforme Confident AI pour automatiser la mesure de la qualité RAG et le suivi des régressions."
**Critères d'Acceptation** :
- [x] Installation de `deepeval` dans `requirements.txt`.
- [x] Exécution de `deepeval login` pour l'envoi des résultats vers **Confident AI**.
- [x] Configuration du `EvaluationDataset` pour charger le `gold_dataset.json`.
- [x] **Implementation Tip** : Utiliser `deepeval.test_case.LLMTestCase` pour encapsuler les résultats (Input, Actual Output, Retrieval Context, Expected Output).

### [PBI-1303] EVAL : Audit "Intégrité Technique" (Source : Gold Dataset)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : M
**User Story** : "En tant qu'expert métier, je veux m'assurer que le bot ne donne aucune fausse information technique sur les PC Portables Jumia."
**Critères d'Acceptation** :
- [x] Utilisation de `deepeval.metrics.FaithfulnessMetric` (Seuil: 0.8) pour l'hallucination.
- [x] Utilisation de `deepeval.metrics.ContextualRecallMetric` (Seuil: 0.7) pour l'oubli.
- [x] Utilisation de `deepeval.metrics.ContextualPrecisionMetric` (Seuil: 0.7) pour le Top 2.
- [x] Utilisation de `deepeval.metrics.AnswerRelevancyMetric` (Seuil: 0.7) pour la pertinence.
- [x] Utilisation de `deepeval.metrics.AnswerCorrectnessMetric` (Seuil: 0.7) pour le score Gold.
- [x] **Technical Guideline** : Créer un script `tests/test_rag_metrics.py` qui itère sur le `gold_dataset.json` et appelle `deepeval.evaluate()`.

### [PBI-1306] TECH : Observabilité & Tracing (Arize Phoenix)
**Status** : DONE ✅
**Priorité** : Medium | **Estimation** : S
**User Story** : "En tant que Lead-Dev, je veux visualiser le cheminement complet de mes requêtes RAG (Tracing) pour identifier les goulots d'étranglement (latence) et les sources d'hallucination."
**Critères d'Acceptation** :
- [x] Installation de `arize-phoenix` et `openinference-instrumentation-llama-index`.
- [x] **Instrumentation Code** : 
  ```python
  from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
  from phoenix.otel import register
  tracer_provider = register(project_name="jumia-rag-companion")
  LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)
  ```
- [x] Accès au dashboard local Phoenix (généralement port 6006) pour l'analyse des traces.
- [x] Capture automatique de la latence et de la consommation de tokens par requête.

### [PBI-2000] LE COMPAGNON NOTEBOOK (Pure Sémantique, Single Sniper, Intent-based & Liens Directs)
**Status** : DONE ✅
**Priorité** : CRITIQUE | **Estimation** : L
**User Story** : "En tant que Personal Shopper Jumia, je veux comprendre l'intention d'usage de l'utilisateur pour lui proposer systématiquement le **meilleur Notebook unique** avec son **lien direct Jumia**, en me basant sur la pertinence technique et la force de conviction."
**Critères d'Acceptation** :
- [x] **Action 1 : Nettoyage & Neutralité (RESET TOTAL)**
  - Retrait définitif du VFM, Trust Score et de la gestion de Localisation (villes).
  - **PURGE TOTALE** : Suppression physique de tous les fichiers `.md` existants dans `data/raw/markdown/notebooks/`.
  - **RESET QDRANT** : Suppression et recréation de la collection `jumia_products`.
- [x] **Action 2 : Intelligence d'Usage**
  - Mappage des intentions (Gaming, Études, Montage) vers des filtres techniques CPU/RAM/GPU.
- [x] **Action 3 : Structure "Single Sniper" & Lien**
  - Présentation obligatoire d'une seule option avec : Nom, Prix, Specs clés et **URL cliquable Jumia**.
- [x] **Action 4 : Ingestion "Controlled Batch"**
  - Scraping et ingestion de **30 articles Notebooks** maximum (Données 100% propres, sans scores).

### [PBI-1200] EVAL : Génération du Dataset Synthétique (Gold Dataset)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : M
**User Story** : "En tant que Lead-Dev, je veux automatiser la création d'un dataset (Question/Contexte/Réponse attendue) pour m'assurer que le bot ne donne pas de fausses informations sur les laptops."
**Critères d'Acceptation** :
- [x] Script de génération synthétique `scripts/generate_test_data.py`.
- [x] Création d'un dataset `tests/gold_dataset.json` (20-30 cas).
- [ ] Mesure automatisée des metrics (S12).

### [PBI-1101] PROMPT : Guide de Traduction "Darija-Tech" (Glossaire)
**Status** : DONE ✅
**Priorité** : Medium | **Estimation** : S
**User Story** : "En tant qu'utilisateur marocain, je veux que le bot utilise des expressions techniques familières (ex: 'ra9a', 'madi', 'tayra') pour que les conseils soient plus naturels."
**Critères d'Acceptation** :
- [ ] Création d'un dictionnaire de correspondance Terme Tech <-> Expression Darija.
- [ ] Intégration du glossaire dans le System Prompt.
- [ ] Test de validation du ton avec le Chef d'Orchestre.

### [PBI-1102] TECH/UX : Intelligence d'Intention & Stabilité (Usage Mapping)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : M
**User Story** : "En tant que client non-expert, je veux exprimer mon besoin (ex: 'pour mes études') et que le bot identifie seul la RAM/CPU nécessaire, tout en profitant d'un système stable sans erreurs de type."
**Critères d'Acceptation** :
- [x] **Fix Stabilité** : Correction de l'erreur de type `RESPONSE_TYPE` dans `src/rag_engine.py` en utilisant le type Union correct de LlamaIndex (`Response | StreamingResponse | AsyncStreamingResponse`).
- [x] **Schéma de Métadonnées** : Définition rigoureuse des `AttributeInfo` pour l'Auto-Retriever (RAM: int, CPU: string, Price: float).
- [x] **Mappage Intention (Prompting)** : Intégration d'un System Prompt dédié à l'Auto-Retriever expliquant les correspondances métier (ex: Gaming = GPU dédié + 16GB RAM).
- [x] **Validation Technique** : Test de l'Auto-Retriever via `VectorIndexAutoRetriever` et vérification des filtres générés dans les logs Phoenix.

### [PBI-1701] TECH/UX : Sawt Jumia (Synthèse Vocale & Multimédia Orchestré)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : L (Découpé en S/M pour Sprint 17)
**User Story** : "En tant qu'utilisateur, je veux recevoir une réponse complète (Image + Texte/Liens + Vocal) pour une aide à l'achat immersive et professionnelle."
**Critères d'Acceptation (Sprint 17)** :
- [x] **[PBI-1701.1] INFRA** : Intégration OpenAI TTS (Modèle `gpt-4o-mini-tts` en format `.opus`).
- [x] **[PBI-1701.2] UX** : Séquençage Multimédia (Image -> Texte -> Vocal) via Evolution API.
- [x] **[PBI-1701.3] PROMPT** : Double flux de sortie (Prosodie pour TTS vs Structure pour WhatsApp).
- [x] **[PBI-1702] EVAL** : Audit de l'expérience multimodale (Vérification liens/images/audio).

### [PBI-1103] TECH : Support Vocal WhatsApp & LLM Darija-Native
**Status** : DONE ✅
**Priorité** : High | **Estimation** : L (Découpé en S/M pour Sprint 16)
**User Story** : "En tant qu'utilisateur, je veux parler en Darija et que le bot comprenne mes nuances culturelles pour me répondre dans un Darija parfait (et non un Français traduit)."
**Critères d'Acceptation (Sprint 16)** :
- [x] **[PBI-1103.1] INFRA** : Intégration API OpenAI Whisper (v1/audio/transcriptions).
- [x] **[PBI-1103.2] PROMPT** : Moteur de Réponse Darija-Native (GPT-4o Full pour le Persona).
- [x] **[PBI-1103.3] UX** : Onboarding Audio & Invitation WhatsApp ("Dwi m3aya b-darija").
- [x] **[PBI-1601] TECH** : Synchronisation client Qdrant v1.10 (Hygiène technique).

### [PBI-000] SPRINT 0 : Infrastructure & Walking Skeleton
**Status** : DONE ✅

### [PBI-101] Crawling & Extraction (10 pages)
**Status** : DONE ✅

### [PBI-110] Scraper v1.1 (Evolution)
**Status** : DONE ✅

### [PBI-120] Architecture Multi-Catégorie & Markdown v2 (Perfection)
**Status** : DONE ✅

### [PBI-130] Extraction Logistique Dynamique (Livraison)
**Status** : CANCELLED ❌ (Simplification technique pour stabilité du scraper v2)

### [PBI-201] Ingestion Hybride (LlamaIndex)
**Status** : DONE ✅

### [PBI-210] Moteur RAG Avancé (Multi-Query & Auto-Retriever)
**Status** : DONE ✅

### [PBI-301] Gateway WhatsApp (Infrastructure)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : L
**User Story** : "En tant que système, je veux être connecté à Evolution API afin de recevoir et d'envoyer des messages réels sur WhatsApp."
**Critères d'Acceptation :**
- [x] Instance Evolution API fonctionnelle (Docker).
- [x] Webhook configuré pour router les messages entrants vers `src/session_manager.py`.
- [x] Envoi de messages texte simple validé via API.

### [PBI-302] Personnalité & Intelligence Commerciale
**Status** : DONE ✅
(Note: Entièrement opérationnel avec la Gateway WhatsApp active)

### [PBI-601] Support des Images sur WhatsApp
**Status** : DONE ✅
**Priorité** : Medium | **Estimation** : M
- Extraction des images produits et envoi via `sendMedia`.

### [PBI-602] Comparaison de Panier Assistée
**Status** : DONE ✅
**Priorité** : Medium | **Estimation** : M
- Logiciel de comparaison par tableau Markdown et verdict Darija.

### [PBI-801] SETUP : Appairage WhatsApp (QR Code)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : S
**User Story** : "En tant que Chef d'Orchestre, je veux scanner un QR Code pour connecter mon numéro WhatsApp au moteur RAG."
**Critères d'Acceptation** :
- [x] Création de l'instance `WHATSAPP-BAILEYS` via `POST /instance/create`.
- [x] Récupération et affichage du QR Code (Base64 ou Terminal).
- [x] Validation de la connexion (`CONNECTION_UPDATE` event).

### [PBI-802] TECH : Exposition du Webhook (Tunneling)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : S
**User Story** : "En tant que système, je veux une URL publique pour recevoir les messages WhatsApp en temps réel."
**Critères d'Acceptation** :
- [x] Mise en place d'un tunnel (Ngrok/LocalTunnel) pointant vers le port FastAPI.
- [x] Configuration du Webhook dans Evolution API (`MESSAGES_UPSERT`, `CONNECTION_UPDATE`).
- [x] Test de connectivité (Ping/Pong).

### [PBI-803] TECH : Récepteur Webhook FastAPI (Performance)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : M
**User Story** : "En tant qu'utilisateur, je veux que le bot réponde sans délai technique (Timeout WhatsApp)."
**Critères d'Acceptation** :
- [x] Endpoint `/webhook` validant les headers de sécurité (`apikey`).
- [x] Utilisation de `BackgroundTasks` pour traiter le RAG après avoir répondu `200 OK` à Evolution API.
- [x] Gestion des messages texte simples et multimédia.

### [PBI-804] UX : Test Live "Mrehba" (Onboarding)
**Status** : DONE ✅
**Priorité** : Medium | **Estimation** : XS
- Accueil interactif "Mrehba" fonctionnel sur WhatsApp.

### [PBI-310] Gestion de la Localisation Utilisateur (Onboarding)
**Status** : CANCELLED ❌ (Retiré le 05/03 pour focus produit strict)
**Priorité** : - | **Estimation** : S

## 📝 FEEDBACKS À AFFINER

### [STYLE/TONE] : Correction du biais de prudence (PBI-402)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : XS
**Feedback Client** : "L'assistant ne doit pas freiner la vente. Dire 'il faut être prudent' pour un produit sans avis est trop négatif."
**Action** : Reformuler la consigne d'honnêteté dans `src/rag_engine.py`. Remplacer l'avertissement par une invitation à la découverte (ex: "Soyez le premier à donner votre avis").

### [PBI-401] TECH/UX : Équilibrage du Re-ranking (Poids Business vs Sémantique)
**Status** : DONE ✅

### [PBI-402] PROMPT/SECURITY : Renforcement de la consigne d'Honnêteté (Trust Score 0)
**Status** : DONE ✅

### [PBI-403] TECH : Affinage de l'Auto-Retriever (Over-filtering)
**Status** : DONE ✅

### [PBI-404] TECH/UX : Seuil de Pertinence Sémantique (Hard-Filtering)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : S
**User Story** : "En tant qu'utilisateur, je veux que les produits sémantiquement faibles (< 0.6) soient éliminés de la liste de re-ranking, même s'ils ont des scores business parfaits."
**Critères d'Acceptation** :
- [x] Définir un seuil de similarité vectorielle (ex: 0.6) dans le `JumiaReRanker`.
- [x] Tout produit en dessous du seuil doit être supprimé de la liste AVANT le calcul du boost business.
- [x] **Test** : Une requête "Crème" ne doit jamais retourner une "Cartouche d'encre" même si cette dernière a un Trust Score de 5.0.

### [PBI-502] TECH/UX : VFM Boost via Expertise Externe (MCP) [REVERTED]
**Status** : CANCELLED ❌ (Décision client du 05/03)
**Priorité** : - | **Estimation** : M
**User Story** : "En tant que Personal Shopper, je veux enrichir le score VFM avec des tests d'experts externes."
**Note** : Fonctionnalité supprimée pour privilégier les données Jumia natives.
