# 👑 Jumia RAG Assistant - Compagnon Notebook

## 🎯 Vision du Projet : "Notebook Companion"
Transformer le catalogue de PC Portables de **Jumia.ma** en une expérience de conseil d'expert. L'assistant agit comme un **Personal Shopper technique** qui aide les utilisateurs marocains à choisir le laptop idéal (Gaming, Études, Bureautique) via une recherche sémantique pure et une expertise technique approfondie.

---

### 🧠 Intelligence de Données & RAG Avancé (Source de Vérité)
Notre moteur est optimisé pour la recommandation de matériel informatique avec une approche centrée sur l'usage :
1.  **🔍 Recherche Sémantique Pure** : Utilisation d'embeddings de haute qualité pour matcher les besoins (ex: "laptop pour montage vidéo") avec les spécifications réelles (CPU/GPU/RAM).
2.  **🏆 Sélection Top 2** : Le système propose systématiquement les deux meilleures options pour faciliter la décision sans surcharge cognitive.
3.  **🇲🇦 Darija Hybrid** : Compréhension naturelle du Darija technique marocain converti en critères de recherche précis.
4.  **🎓 Expertise Technique** : Intégration de guides d'achat et d'insights d'experts pour justifier chaque recommandation.

---

### ✅ État du Projet (Sprint 12 : Hygiène & Alignement)
Le projet a évolué d'un assistant généraliste vers un **expert spécialisé en Notebooks**.
- [x] **Extraction Robuste** : Utilisation de Crawl4AI pour un scraping structuré et précis.
- [x] **Moteur Auto-RAG** : Filtrage intelligent par métadonnées (Prix, RAM, SSD, État).
- [x] **Zéro Localisation** : Suppression des flux logistiques pour se concentrer sur le conseil produit pur.
- [x] **Connectivité WhatsApp** : Intégration via Evolution API opérationnelle.

---

### 🛠️ Stack Technique
- **Backend** : Python 3.12+ / FastAPI.
- **RAG Orchestration** : [LlamaIndex](https://www.llamaindex.ai/) (Multi-Query & Auto-Retriever).
- **Vector DB** : [Qdrant](https://qdrant.tech/) (Recherche hybride & filtrage métadonnées).
- **Extraction** : [Crawl4AI](https://crawl4ai.com/) + GPT-4o-mini pour la conversion Markdown.
- **WhatsApp Gateway** : [Evolution API](https://evolution-api.com/).

---

### 🚀 Installation & Lancement
```bash
# Setup environnement
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Lancement de la démo locale
python src/main.py
```

---
*Dernière mise à jour : 2026-03-08 (Sprint 12 - Hygiène & Alignement)*
