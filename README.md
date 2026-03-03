# 👑 Jumia RAG Assistant - Moteur de Shopping Intelligent

## 🎯 Vision du Projet
Transformer le catalogue multi-catégories de **Jumia.ma** en un assistant personnel de shopping conversationnel. L'assistant utilise le **RAG (Retrieval-Augmented Generation)** pour conseiller, comparer et recommander les meilleurs produits aux utilisateurs marocains avec un ton expert, amical et local (Darija/Français).

---

### 🧠 Intelligence de Données & RAG Avancé (Source de Vérité)
Notre moteur est aujourd'hui capable de traiter des requêtes complexes grâce à une structuration profonde de la donnée :
1.  **📊 Scoring Business** : Calcul du `Trust Score` (fiabilité) et `Value for Money` intégré directement dans le re-ranking.
2.  **🧠 RAG Hybride** : Multi-Query Expansion (Darija -> Français technique) et Hard-Filtering (Seuil 0.8) pour éliminer les produits hors-sujet.
3.  **🇲🇦 Localisation** : Système d'onboarding par dialogue pour identifier la ville de l'utilisateur.

---

### 🚧 État de la Gateway (Sprint 7 en cours)
**L'intégration WhatsApp est la priorité actuelle.** 
Le projet utilise **Evolution API** comme passerelle cible. 
- [ ] **Sprint 7 (Objectif)** : Établir la connexion réelle entre le moteur RAG et WhatsApp via Evolution API.
- [ ] **Next Step** : Une fois la gateway active, nous déploierons le support multimédia (photos produits).

---

### 🛠️ Stack Technique
- **Backend** : Python 3.12+ / FastAPI.
- **RAG Orchestration** : [LlamaIndex](https://www.llamaindex.ai/).
- **Vector DB** : [Qdrant](https://qdrant.tech/) (Recherche hybride).
- **Extraction** : [Crawl4AI](https://crawl4ai.com/) + GPT-4o-mini.
- **WhatsApp Target** : [Evolution API](https://evolution-api.com/).

---

### 🚀 Installation & Diagnostic
```bash
# Setup environnement
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Vérification de l'infrastructure
python scripts/check_infra.py
```

---
*Dernière mise à jour : 2026-03-03 (Sprint 7 - Infra & Connectivité)*
