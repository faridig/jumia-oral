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

## ✅ DEFINITION OF DONE (DoD)
- Extraction : Données structurées validées par le schéma Pydantic.
- RAG : Capacité de comparaison entre 2 produits via le LLM.
- UX : Chatbot réactif sur WhatsApp avec gestion du contexte utilisateur.
- Sécurité : Variables d'environnement pour toutes les clés API.
- **Sales Compliance** : Aucun nom de concurrent ou prix externe ne doit filtrer dans les réponses.
- **Qualité de Recommandation** : Aucun produit avec une similarité sémantique faible ne doit polluer les résultats (Hard-Filtering).

## 📋 BACKLOG GÉNÉRAL

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
**Status** : PENDING ⏳
**Priorité** : High | **Estimation** : L
**User Story** : "En tant que système, je veux être connecté à Evolution API afin de recevoir et d'envoyer des messages réels sur WhatsApp."
**Critères d'Acceptation** :
- [ ] Instance Evolution API fonctionnelle (Docker).
- [ ] Webhook configuré pour router les messages entrants vers `src/session_manager.py`.
- [ ] Envoi de messages texte simple validé via API.

### [PBI-302] Personnalité & Intelligence Commerciale
**Status** : DONE ✅
(Note: La logique de réponse est prête, mais attend le canal de diffusion PBI-301)

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
