# 🚀 BACKLOG - JUMIA RAG PROJECT

## ⚙️ CONFIGURATION TECHNIQUE
- **Langage** : Python 3.10+
- **Framework Scraping** : Crawl4AI avec **LLMExtractionStrategy** (GPT-4o-mini).
- **Orchestration RAG** : LlamaIndex avec **Hybrid Search** (Dense + Sparse).
- **Vector Database** : Qdrant (Utilisation de l'instance locale existante).
- **Isolation des données** : Collection dédiée `jumia_products`.
- **WhatsApp Gateway** : Evolution API (Open Source Baileys-based).
- **Mémoire Conversationnelle** : SimpleChatStore (Persistance JSON par numéro).
- **Format de sortie** : Markdown avec Frontmatter YAML (metadata enrichies).

## 🏛️ JOURNAL DES DÉCISIONS
1. **[2026-02-26] Choix de Crawl4AI & LLM Extraction** : Pour garantir l'extraction des avis profonds et des specs techniques sans maintenance de sélecteurs.
2. **[2026-02-26] WhatsApp via Evolution API** : Solution Open Source robuste pour transformer WhatsApp en canal de vente conversationnel.
3. **[2026-02-26] Score de Confiance** : Implémentation d'un calcul `(Note * 0.7) + (log10(Avis) * 0.3)` pour classer les "meilleurs produits".
4. **[2026-02-26] Ton Amical Marocain** : Personnalité "Personal Shopper" mixant Français et Darija.
5. **[2026-02-28] Architecture Category-Agnostic** : Le schéma de données est conçu pour être extensible (Informatique, Cosmétique, Bricolage) en séparant les `core_metadata` (universels) des `category_specs` (dynamiques).
6. **[2026-02-28] Normalisation via LLM** : L'extraction LLM doit forcer des unités standards (GB, MAD, ml, kg) pour permettre des calculs et des filtres numériques fiables dans le RAG.
7. **[2026-02-28] Pivot RAG Avancé** : Intégration de Multi-Query Expansion et Auto-Retriever pour compenser les variations de langage (Darija/Français).
8. **[2026-03-01] VFM Boost via MCP (Sales-Focused)** : Décision d'intégrer une recherche web via MCP pour enrichir le VFM avec des avis d'experts mondiaux et des arguments de vente "sociaux", SANS jamais citer de prix concurrents, afin de maximiser la conversion sur Jumia.
9. **[2026-03-01] Seuil de Pertinence (Hard-Filter)** : Constat (Sprint 4) que le Trust Score peut biaiser les résultats vers des produits hors-sujet. Décision d'implémenter un filtre de similarité minimum avant le re-ranking.

10. **[2026-03-04] Pivot Spécialisé PC Portables** : Décision de restreindre le catalogue RAG uniquement aux ordinateurs portables (`notebooks`) pour garantir une précision technique maximale (CPU, RAM, GPU) et une expertise verticale.
11. **[2026-03-04] Réinitialisation Totale (Reset Data)** : Purge du dossier `data/` et de la collection Qdrant pour éliminer les anciennes données multi-catégories et repartir sur une base 100% Notebooks.
12. **[2026-03-04] Transition Chat-Centric (PBI-1001)** : Abandon du modèle de requête unique pour un moteur de chat contextuel. Cette décision vise à transformer le bot en un véritable compagnon d'achat capable de gérer des dialogues complexes.

## ✅ DEFINITION OF DONE (DoD)
- Extraction : Données structurées validées par le schéma Pydantic (Enrichi Laptop).
- RAG : Capacité de comparaison entre 2 modèles de PC (ex: i5 vs i7).
- UX : Chatbot réactif sur WhatsApp avec gestion du contexte utilisateur.
- Sécurité : Variables d'environnement pour toutes les clés API.
- **Laptop Expertise** : Le bot doit être capable d'expliquer les différences techniques (RAM DDR4 vs DDR5, SSD NVMe) en Darija.
- **Sales Compliance** : Aucun nom de concurrent ou prix externe ne doit filtrer dans les réponses.
- **Qualité de Recommandation** : Aucun produit avec une similarité sémantique faible ne doit polluer les résultats (Hard-Filtering).

## 📋 BACKLOG GÉNÉRAL

### [PBI-901] TECH : Purge & Reset (Clean Slate)
**Status** : PENDING ⏳
**Priorité** : High | **Estimation** : XS
**User Story** : "En tant que Lead-Dev, je veux vider les données obsolètes pour garantir que mon moteur RAG ne recommande que des PC Portables."
**Critères d'Acceptation** :
- [ ] Suppression physique des fichiers `.md` et `.csv` dans `data/`.
- [ ] Suppression et re-création de la collection `jumia_products` dans Qdrant.

### [SPIKE-902] TEST : Extraction "Micro-Batch" (10 Produits)
**Status** : PENDING ⏳
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
**Status** : PENDING ⏳
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
**Status** : DONE ✅
**Priorité** : Medium | **Estimation** : S
- Flux d'onboarding demandant la ville à l'utilisateur lors du premier échange.
- Persistance de la localisation dans le `SimpleChatStore`.

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

### [PBI-502] TECH/UX : VFM Boost via Expertise Externe (MCP - Sales Focus)
**Status** : DONE ✅
**Priorité** : High | **Estimation** : M
**User Story** : "En tant que Personal Shopper, je veux enrichir le score VFM avec des tests d'experts externes, afin de rassurer l'utilisateur et de **déclencher l'achat sur Jumia**."
**Critères d'Acceptation** :
- [x] Utiliser le MCP pour trouver des notes de tests professionnels (ex: DXOMARK, NotebookCheck).
- [x] Extraire 2-3 arguments "chocs" (Pros/Cons) pour chaque produit.
- [x] **Arbitrage de Confiance** : Si des avis experts sont trouvés, transformer le message "Manque d'avis" (PBI-402) en argument de "Nouveauté validée par les pros".
- [x] Interdiction stricte de citer des prix concurrents ou des noms de boutiques externes.
- [x] Intégrer ces arguments dans la réponse WhatsApp pour "vendre" le produit sélectionné.


