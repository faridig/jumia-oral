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
18. **[2026-03-05] Support Vocal & Darija Natif** : Décision d'intégrer le support des messages vocaux (STT). Le système doit être capable de comprendre le Darija parlé (via Whisper ou équivalent performant) et de répondre avec une structure grammaticale Darija authentique, dépassant le simple mélange de mots.
19. **[2026-03-05] Recherche par Intention d'Usage** : Transition d'une recherche par mots-clés vers une compréhension des besoins métiers (Gaming, Montage, Études) pour filtrer automatiquement les specs techniques requises.
20. **[2026-03-05] Stratégie "Full-Context Chunking"** : Abandon du découpage par phrases ou sections. Chaque fiche Notebook Jumia (< 2000 tokens) sera ingérée comme un **Node unique**. Cela garantit que le LLM a accès à toutes les specs techniques et à l'URL Jumia sans répétition inutile ou perte de lien entre les métadonnées et le descriptif.
21. **[2026-03-05] Épuration de la Sentiment Analysis (Pure Rationale)** : Pour être cohérent avec le retrait du VFM et du Trust Score, les **notes numériques** (scores 0-10) et l'axe **"Value"** sont supprimés de l'analyse de sentiment. On ne conserve que le **Rationale** (texte descriptif) pour les axes techniques (Performance, Build Quality, Display) afin de nourrir le RAG en arguments qualitatifs neutres.
22. **[2026-03-06] Choix Technologique Gold Dataset (PBI-1200)** : Pour favoriser la montée en compétence technique et la maîtrise du style Darija, l'option **Script Python Sur-Mesure + OpenAI** est choisie à la place des outils natifs (LlamaIndex Generator) ou spécialisés (DeepEval). Cela permet un contrôle total sur l'extraction des specs critiques (RAM, CPU, Prix) et sur la langue de la question.

## ✅ DEFINITION OF DONE (DoD)
- Extraction : Données structurées validées par le schéma Pydantic (Enrichi Laptop).
- RAG : Capacité de comparaison entre 2 modèles de PC (ex: i5 vs i7).
- UX : Chatbot réactif sur WhatsApp avec gestion du contexte utilisateur.
- Sécurité : Variables d'environnement pour toutes les clés API.
- **Laptop Expertise** : Le bot doit être capable d'expliquer les différences techniques (RAM DDR4 vs DDR5, SSD NVMe) en Darija.
- **Sales Compliance** : Aucun nom de concurrent ou prix externe ne doit filtrer dans les réponses.
- **Pertinence Pure** : Seule la similarité sémantique et les caractéristiques techniques réelles (CPU, RAM, Prix) guident la recommandation.
- **Dual Proposal** : Chaque recommandation doit systématiquement présenter les deux meilleures options trouvées, en soulignant leurs différences.

## 📋 BACKLOG GÉNÉRAL

### [PBI-901] TECH : Purge & Reset (Clean Slate)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : XS
**User Story** : "En tant que Lead-Dev, je veux vider les données obsolètes pour garantir que mon moteur RAG ne recommande que des PC Portables."
**Critères d'Acceptation** :
- [ ] Suppression physique des fichiers `.md` et `.csv` dans `data/`.
- [ ] Suppression et re-création de la collection `jumia_products` dans Qdrant.

### [SPIKE-902] TEST : Extraction "Micro-Batch" (10 Produits)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : XS
**User Story** : "En tant que Chef d'Orchestre, je veux tester l'extraction LLM sur 10 produits pour valider la structure des métadonnées PC sans gaspiller de tokens."
**Critères d'Acceptation** :
- [ ] Limiter le scraping aux 10 premiers produits de Jumia Notebooks.
- [ ] Générer un rapport JSON des métadonnées extraites (CPU, RAM, SSD, GPU, Écran).
- [ ] Validation manuelle du résultat par le Chef d'Orchestre avant passage à l'échelle.

### [PBI-902b] SCRAPING : Extraction Totale "Notebooks" (5 Pages)
**Status** : PENDING ⏳
**Priorité** : High | **Estimation** : M
**User Story** : "En tant que Personal Shopper, je veux extraire les fiches techniques des 5 premières pages de Jumia Notebooks après validation du Spike."
**Critères d'Acceptation** :
- [ ] Crawling de `https://www.jumia.ma/notebooks/`.
- [ ] Extraction LLM basée sur la structure validée au Spike.
- [ ] Stockage structuré dans `data/`.

### [PBI-903] INGESTION : Indexation Vectorielle PC Portables
**Status** : DONE ✅
**Priorité** : High | **Estimation** : M
- Ingestion des nouvelles données dans le moteur RAG.
- Vérification de la recherche hybride sur des requêtes techniques (ex: "PC i7 16GB").

### [PBI-1001] TECH/UX : Mémoire Contextuelle de Recherche (Shopping Dialogue)
**Status** : PENDING ⏳
**Priorité** : High | **Estimation** : M

**User Story** : "En tant que Personal Shopper, je veux que le bot se souvienne des produits précédemment cités, afin que l'utilisateur puisse poser des questions de suivi (ex: 'Et son autonomie ?') sans répétition fastidieuse."

**Dépendances** : PBI-210 (Moteur RAG)

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Question de suivi sur un produit**
  - **GIVEN** L'utilisateur a déjà reçu une description du "MacBook Air M2".
  - **WHEN** L'utilisateur demande : "Et son autonomie ?".
  - **THEN** Le bot identifie que "son" se rapporte au MacBook Air M2 et répond via le RAG sur ce contexte précis.
- [ ] **Scenario 2 : Transition vers ContextChatEngine**
  - **GIVEN** Le `src/rag_engine.py` utilise un `QueryEngine`.
  - **WHEN** On initialise le moteur RAG.
  - **THEN** Il doit exposer une interface `chat` (LlamaIndex ContextChatEngine) au lieu de `query`.
- [ ] **Scenario 3 : Persistence de l'historique**
  - **GIVEN** Un utilisateur WhatsApp identifié par son numéro.
  - **WHEN** Plusieurs échanges ont lieu.
  - **THEN** Le `SimpleChatStore` doit sauvegarder et recharger l'historique pour maintenir la cohérence sur plusieurs jours.

### [PBI-1002] TECH : Nettoyage & Retrait Context7 (Expert Advisor)
**Status** : PENDING ⏳
**Priorité** : High | **Estimation** : S
**User Story** : "En tant que Lead-Dev, je veux supprimer les appels à l'Expert Advisor (MCP) dans le moteur RAG pour me baser uniquement sur les descriptions Jumia."
**Critères d'Acceptation** :
- [ ] Suppression de l'injection du `expert_node` dans `src/rag_engine.py`.
- [ ] Désactivation/Suppression de `src/expert_advisor.py`.
- [ ] Validation que les réponses LLM ne citent plus de sources externes.

### [PBI-1003] TECH : Suppression totale du Score VFM
**Status** : DONE ✅
**Priorité** : High | **Estimation** : S
**User Story** : "En tant que Lead-Dev, je veux retirer toute trace du score VFM (calcul, stockage et re-ranking) pour simplifier le modèle de données."
**Critères d'Acceptation** :
- [x] Retrait du champ `value_for_money_score` dans le schéma Pydantic (`models.py`).
- [x] Suppression de l'instruction d'extraction VFM dans `src/scraper.py`.
- [x] Mise à jour du `JumiaReRanker` dans `src/rag_engine.py` (Neutralisé au profit d'une sémantique technique pure).
- [x] Nettoyage de l'ingestion (`src/ingestion.py`).

### [PBI-1004] TECH : Suppression totale du Trust Score
**Status** : DONE ✅
**Priorité** : High | **Estimation** : S
**User Story** : "En tant que Lead-Dev, je veux supprimer le Trust Score et le JumiaReRanker pour ne garder que la pertinence sémantique LlamaIndex."
**Critères d'Acceptation** :
- [x] Suppression de la fonction `calculate_trust_score` dans `src/scraper.py`.
- [x] Retrait de `trust_score` du modèle de données et du frontmatter Markdown.
- [x] Suppression (ou neutralisation) du `JumiaReRanker` dans `src/rag_engine.py`.
- [x] Mise à jour du prompt système pour ne plus mentionner les scores ou l'absence d'avis.

### [PBI-1005] UX : Implémentation de la réponse "Dual-Choice"
**Status** : PENDING ⏳
**Priorité** : High | **Estimation** : S
**User Story** : "En tant que Personal Shopper, je veux proposer systématiquement les 2 meilleures options au client, afin de faciliter son choix par la comparaison."
**Critères d'Acceptation** :
- [ ] Ajuster le `response_synthesizer` pour forcer la présentation de 2 produits.
- [ ] Modifier le prompt de personnalité pour structurer la réponse avec : Option 1, Option 2, et un court conseil technique pour départager.
- [ ] Gérer le cas où un seul produit est trouvé (réponse adaptée).

### [PBI-1006] TECH/UX : Retrait de la gestion de Localisation
**Status** : IN_PROGRESS 🏗️
**Priorité** : High | **Estimation** : XS
**User Story** : "En tant que Lead-Dev, je veux supprimer le flux d'onboarding lié à la ville et toute mention de localisation dans les réponses, pour me concentrer exclusivement sur les produits."
**Critères d'Acceptation** :
- [ ] Suppression du flux de demande de ville dans `src/session_manager.py`.
- [ ] Retrait de la persistance de localisation dans le `SimpleChatStore`.
- [ ] Mise à jour du prompt système pour interdire toute mention de ville ou de logistique locale.

### [PBI-1201] DOC : Refonte du README.md (Alignement Vision Notebook)
**Status** : IN_PROGRESS 🏗️
**Priorité** : High | **Estimation** : S
**User Story** : "En tant qu'utilisateur, je veux un README à jour afin de comprendre la vision réelle du projet (Notebook Companion) sans être induit en erreur par d'anciennes fonctionnalités supprimées."
**Critères d'Acceptation** :
- [ ] Suppression des mentions Trust Score et VFM (obsolètes).
- [ ] Suppression des sections sur la Localisation (villes, livraison).
- [ ] Mise à jour de la Stack Technique (Crawl4AI, LlamaIndex Hybrid, Evolution API).
- [ ] Actualisation de l'état d'avancement et de la vision "Pure Sémantique".

### [PBI-1202] TECH : Nettoyage src/main.py (Alignement Démo)
**Status** : IN_PROGRESS 🏗️
**Priorité** : High | **Estimation** : XS
**User Story** : "En tant que développeur, je veux que le script de démo reflète le flux actuel du bot (sans localisation) pour éviter des erreurs d'exécution ou de compréhension."
**Critères d'Acceptation** :
- [ ] Retrait du message "Ana f Casablanca" et de la logique d'onboarding ville.
- [ ] Mise à jour des messages de test pour se concentrer sur la recherche de Notebooks.
- [ ] Mise à jour du print d'entête (Sprint 12).

### [PBI-2000] LE COMPAGNON NOTEBOOK (Pure Sémantique, Dual-Choice, Intent-based & Liens Directs)
**Status** : DONE ✅
**Priorité** : CRITIQUE | **Estimation** : L
**User Story** : "En tant que Personal Shopper Jumia, je veux comprendre l'intention d'usage de l'utilisateur pour lui proposer systématiquement les **deux meilleurs Notebooks** avec leurs **liens directs Jumia**, sans aucun biais de score, en me basant uniquement sur la pertinence technique."
**Critères d'Acceptation** :
- [x] **Action 1 : Nettoyage & Neutralité (RESET TOTAL)**
  - Retrait définitif du VFM, Trust Score et de la gestion de Localisation (villes).
  - **PURGE TOTALE** : Suppression physique de tous les fichiers `.md` existants dans `data/raw/markdown/notebooks/`.
  - **RESET QDRANT** : Suppression et recréation de la collection `jumia_products`.
- [x] **Action 2 : Intelligence d'Usage**
  - Mappage des intentions (Gaming, Études, Montage) vers des filtres techniques CPU/RAM/GPU.
- [x] **Action 3 : Structure "Top 2" & Liens**
  - Présentation obligatoire de 2 options avec : Nom, Prix, Specs clés et **URL cliquable Jumia**.
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
**Status** : PENDING ⏳
**Priorité** : Medium | **Estimation** : S
**User Story** : "En tant qu'utilisateur marocain, je veux que le bot utilise des expressions techniques familières (ex: 'ra9a', 'madi', 'tayra') pour que les conseils soient plus naturels."
**Critères d'Acceptation** :
- [ ] Création d'un dictionnaire de correspondance Terme Tech <-> Expression Darija.
- [ ] Intégration du glossaire dans le System Prompt.
- [ ] Test de validation du ton avec le Chef d'Orchestre.

### [PBI-1102] RAG : Mappage "Usage" vers "Specs" (Intention)
**Status** : PENDING ⏳
**Priorité** : High | **Estimation** : M
**User Story** : "En tant que client non-expert, je veux exprimer mon besoin (ex: 'pour mes études') et que le bot identifie seul la RAM/CPU nécessaire."
**Critères d'Acceptation** :
- [ ] Implémenter une couche de raisonnement LLM qui transforme une intention d'usage en filtres techniques (ex: Études -> i3/R3 + 8GB).
- [ ] Intégration dans l'Auto-Retriever de LlamaIndex.

### [PBI-1103] TECH : Support Vocal WhatsApp & LLM Darija-Native
**Status** : PENDING ⏳
**Priorité** : Medium | **Estimation** : L
**User Story** : "En tant qu'utilisateur, je veux parler en Darija et que le bot comprenne mes nuances culturelles pour me répondre dans un Darija parfait (et non un Français traduit)."
**Critères d'Acceptation** :
- [ ] Intégration de Whisper (ou API spécialisée) pour la transcription fidèle du Darija parlé.
- [ ] Sélection/Fine-tuning du prompt pour un LLM (GPT-4o ou modèle spécialisé) capable de traiter la grammaire Darija sans passer par une traduction intermédiaire en Français.
- [ ] Réponse générée en Darija fluide (Latin ou Arabe selon préférence user) respectant les codes de politesse marocains.
- [ ] Validation de la compréhension des expressions idiomatiques ("mkhyr", "3la 9d l-jib", etc.).

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
**Critères d'Acceptation** :
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



