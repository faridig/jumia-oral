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
6. **[2026-02-28] Architecture Category-Agnostic** : Le schéma de données est conçu pour être extensible (Informatique, Cosmétique, Bricolage) en séparant les `core_metadata` (universels) des `category_specs` (dynamiques).
7. **[2026-02-28] Normalisation via LLM** : L'extraction LLM doit forcer des unités standards (GB, MAD, ml, kg) pour permettre des calculs et des filtres numériques fiables dans le RAG.

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
**Priorité** : High | **Estimation** : L
- Crawl des 10 premières pages par catégorie.
- Extraction LLM (GPT-4o-mini) : Specs, Prix, Avis, Score.
- Génération des fichiers `.md` structurés.

### [PBI-110] Scraper v1.1 (Evolution)
**Status** : DONE ✅
**Priorité** : Medium | **Estimation** : S
- Support multi-images (galerie).
- Extraction infos vendeur (score, vitesse, abonnés).
- Expansion dynamique des avis (JS injection).
- Augmentation de la limite de batch.

### [PBI-120] Architecture Multi-Catégorie & Markdown v2 (Perfection)
**Priorité** : High | **Estimation** : M
- **Refactorisation Multi-Catégorie** : Design d'un schéma extensible (Informatique, Cosmétique, Bricolage, etc.) via `category_specific_specs`.
- **Standardisation & Normalisation** : Utilisation du LLM pour transformer les specs brutes en valeurs numériques normalisées (ex: "8Go" -> 8 GB).
- **Logique "Master Product"** : Détection et groupement des offres identiques (Vendeurs multiples) pour un même modèle.
- **Analyse de Sentiment par Axe** : Extraction de scores (1-5) sur des critères précis (Performance, Design, Autonomie, Prix).
- **Calcul de Valeur (Value-Score)** : Algorithme croisant Specs, Prix et Trust Score pour identifier les "Best Deals".

### [PBI-130] Extraction Logistique Dynamique (Livraison)
**Priorité** : Medium | **Estimation** : M
- Script d'interaction JS (Crawl4AI) pour sélectionner les 5 régions clés (Casablanca, Rabat, Tanger, Marrakech, Agadir).
- Extraction d'un tarif "Plafond" (Zone 3 - ex: Dakhla) pour les villes non listées.
- Extraction des frais de livraison et délais par produit.
- Stockage structuré dans le YAML (`shipping_fees`).

### [PBI-201] Ingestion Hybride (LlamaIndex)
**Priorité** : High | **Estimation** : M
- Pipeline Hybrid Search (Vector + Metadata filtering).
- Indexation dans Qdrant.

### [PBI-301] Gateway WhatsApp & Personnalité
**Priorité** : High | **Estimation** : L
- Webhook FastAPI pour Evolution API.
- Prompt System "Personal Shopper Marocain".
- Gestion de la mémoire via SimpleChatStore.

### [PBI-310] Gestion de la Localisation Utilisateur (Onboarding)
**Priorité** : Medium | **Estimation** : S
- Flux d'onboarding demandant la ville à l'utilisateur lors du premier échange.
- Persistance de la localisation dans le `SimpleChatStore`.
- Utilisation automatique de la localisation pour filtrer les frais de livraison dans les réponses.
