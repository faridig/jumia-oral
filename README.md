# 👑 Jumia RAG Assistant - WhatsApp (MVP)

## 🎯 Vision du Projet
Transformer le catalogue informatique de **Jumia.ma** en un assistant personnel de shopping conversationnel sur **WhatsApp**. L'assistant utilise le **RAG (Retrieval-Augmented Generation)** pour conseiller, comparer et recommander les meilleurs produits aux utilisateurs marocains avec un ton amical et local.

---

### 🌊 Flux de Données "Intelligent" (Scraping to RAG)

Notre architecture repose sur une transformation profonde de la donnée brute en information structurée pour l'IA :

1.  **🕵️ Découverte (Crawl4AI)** : Parcours des 10 premières pages par catégorie pour collecter les URLs uniques (~400 produits).
2.  **⚡ Extraction Deep Scan (LLM)** : Utilisation de `gpt-4o-mini` pour transformer le HTML complexe en Markdown structuré.
3.  **📊 Trust Scoring** : Calcul automatique de la fiabilité `(Note * 0.7) + (log10(Nombre d'Avis) * 0.3)`.
4.  **📚 RAG-Ready Markdown** : Génération de fichiers `.md` optimisés pour l'ingestion vectorielle (Metadata + Headers).

---

### 🚀 Optimisation RAG : Le Standard "RAG-Ready"

Pour garantir une précision maximale et éviter les hallucinations, chaque produit est stocké selon une structure stricte facilitant le **Metadata Filtering** et le **Smart Chunking**.

#### Exemple de Structure Produit (`v2` Multi-Catégorie)

```markdown
---
# Core Metadata (Universel)
product_id: "JUM-HP-15-2024"
brand: "HP"
model: "Pavilion 15"
price_numeric: 5499
currency: "MAD"
category: "Laptops"
trust_score: 4.8
review_count: 142
stock_status: "En Stock"

# Category Specs (Dynamique & Normalisé)
category_specs:
  ram: 16
  ram_unit: "GB"
  storage: 512
  storage_unit: "GB"
  cpu: "Intel Core i5"

# Insights (Scores 1-5)
insights:
  performance: 4.5
  design: 4.0
  battery: 3.5
  value_for_money: 4.8

# Logistique
shipping_fees:
  casablanca: 29
  rabat: 35
  marrakech: 39
  tanger: 42
  agadir: 45
  other_zone_3: 59
last_updated: "2026-02-28"
---
```


# HP Pavilion 15 - Intel Core i5 (12th Gen) - 16GB RAM - 512GB SSD

## 🛠️ Caractéristiques Techniques
> **Contexte** : HP Pavilion 15 (Note: 4.8/5)

- **Processeur** : Intel Core i5-1235U (jusqu'à 4.4 GHz)
- **Mémoire Vive** : 16 Go DDR4
- **Stockage** : 512 Go SSD NVMe
- **Écran** : 15.6" Full HD Micro-edge
- **Clavier** : AZERTY Rétroéclairé

## 🌟 Avis Clients & Analyse
> **Contexte** : HP Pavilion 15 (Basé sur 142 avis)

- **Points Forts** : Performance fluide pour le multitâche, écran très lumineux, design élégant.
- **Points Faibles** : Autonomie un peu juste en mode gaming léger (4-5h), ventilateur audible en charge.
- **Résumé** : Excellent rapport qualité/prix pour les étudiants et professionnels.

## 💰 Offre Commerciale
- **Prix Actuel** : 5499 MAD (Anciennement 6200 MAD)
- **Vendeur** : Jumia Official Store (Score: 92%)
- **Lien** : [Voir sur Jumia.ma](https://www.jumia.ma/hp-pavilion-15-...)
```

**Pourquoi ce format ?**
- **Filtrage Précis** : Le Frontmatter YAML permet de répondre instantanément à "Trouve moi un PC à moins de 6000 MAD".
- **Chunking Contextuel** : Le découpage par Headers (`##`) permet au RAG de ne récupérer que la section "Avis" si l'utilisateur pose une question sur la fiabilité.
- **Zéro Perte de Contexte** : L'injection du nom du produit dans chaque section garantit que le LLM sait de quoi il parle, même sur un petit fragment de texte.

---

## ⚙️ Stack Technique
- **Scraping** : [Crawl4AI](https://crawl4ai.com/) + LLM Extraction (GPT-4o-mini).
- **IA Orchestration** : [LlamaIndex](https://www.llamaindex.ai/).
- **Vector DB** : [Qdrant](https://qdrant.tech/) (Recherche hybride Dense/Sparse).
- **WhatsApp** : [Evolution API](https://evolution-api.com/) (Open Source).
- **Backend** : FastAPI (Python 3.12+).

---

## 🚀 Installation & Développement

### 1. Prérequis
- Python 3.12+
- Docker & Docker Compose

### 2. Initialisation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 3. Lancement de l'infrastructure
L'infrastructure utilise une instance Qdrant existante (port 6343). Lancez Evolution API (WhatsApp) :
```bash
docker compose up -d
```

### 4. Vérification
Exécutez le script de diagnostic :
```bash
python scripts/check_infra.py
```

---

## 🇲🇦 Personnalité
L'assistant parle un français chaleureux avec des touches de **Darija** (Mrehba, Besseha, Chouf), agissant comme un expert de confiance ("Personal Shopper").

---
*Projet en cours de développement (Sprint 1 - Scraping & RAG Ready).*
