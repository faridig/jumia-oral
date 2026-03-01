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

## ✅ DEFINITION OF DONE (DoD)
- Extraction : Données structurées validées par le schéma Pydantic.
- RAG : Capacité de comparaison entre 2 produits via le LLM.
- UX : Chatbot réactif sur WhatsApp avec gestion du contexte utilisateur.
- Sécurité : Variables d'environnement pour toutes les clés API.

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

### [PBI-301] Gateway WhatsApp & Personnalité
**Status** : DONE ✅

### [PBI-310] Gestion de la Localisation Utilisateur (Onboarding)
**Status** : PENDING
**Priorité** : Medium | **Estimation** : S
- Flux d'onboarding demandant la ville à l'utilisateur lors du premier échange.
- Persistance de la localisation dans le `SimpleChatStore`.

## 📝 FEEDBACKS À AFFINER

### [PBI-401] TECH/UX : Équilibrage du Re-ranking (Poids Business vs Sémantique)
**Status** : IN PROGRESS 🏃
**Priorité** : Medium | **Estimation** : S

### [PBI-402] PROMPT/SECURITY : Renforcement de la consigne d'Honnêteté (Trust Score 0)
**Status** : IN PROGRESS 🏃
**Priorité** : High | **Estimation** : XS

### [PBI-403] TECH : Affinage de l'Auto-Retriever (Over-filtering)
**Status** : IN PROGRESS 🏃
**Priorité** : Medium | **Estimation** : S
