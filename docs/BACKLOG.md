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
5. **[2026-02-26] Data Isolation** : Utilisation d'une collection Qdrant dédiée pour ne pas interférer avec les autres données de l'utilisateur.

## ✅ DEFINITION OF DONE (DoD)
- Extraction : Données structurées validées par le schéma Pydantic.
- RAG : Capacité de comparaison entre 2 produits via le LLM.
- UX : Chatbot réactif sur WhatsApp avec gestion du contexte utilisateur.
- Sécurité : Variables d'environnement pour toutes les clés API.

## 📋 BACKLOG GÉNÉRAL

### [PBI-000] SPRINT 0 : Infrastructure & Walking Skeleton
**Priorité** : High | **Estimation** : S
- Créer l'arborescence du projet.
- Configurer Docker (Evolution API uniquement).
- Valider la connexion au Qdrant local existant (Collection: `jumia_products`).

### [PBI-101] Crawling & Extraction (10 pages)
**Priorité** : High | **Estimation** : L
- Crawl des 10 premières pages par catégorie.
- Extraction LLM (GPT-4o-mini) : Specs, Prix, Avis, Score.
- Génération des fichiers `.md` structurés.

### [PBI-201] Ingestion Hybride (LlamaIndex)
**Priorité** : High | **Estimation** : M
- Pipeline Hybrid Search (Vector + Metadata filtering).
- Indexation dans Qdrant.

### [PBI-301] Gateway WhatsApp & Personnalité
**Priorité** : High | **Estimation** : L
- Webhook FastAPI pour Evolution API.
- Prompt System "Personal Shopper Marocain".
- Gestion de la mémoire via SimpleChatStore.
