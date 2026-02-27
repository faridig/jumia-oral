# 🏃 SPRINT PLAN - SPRINT 1 (SCRAPING INTELLIGENT)

## 🎯 OBJECTIF
Extraire les données produits de la catégorie "Informatique" de Jumia.ma sur les 10 premières pages en utilisant une extraction intelligente.

## 📋 TÂCHES À RÉALISER

### [PBI-101] Crawling des URLs (Pagination)
- **Tâches** :
  - [ ] Implémenter le crawler de liste pour `https://www.jumia.ma/ordinateurs-accessoires-informatique/`.
  - [ ] Gérer la boucle de pagination pour les pages 1 à 10.
  - [ ] Extraire et stocker la liste unique des URLs produits.
  - [ ] **Logging & Reporting** : Créer `logs/extraction.log` pour suivre la progression page par page et `data/extraction_summary.json` pour le bilan final.

### [PBI-102] Scraping LLM-Powered (Détails & Avis)
- **Tâches** :
  - [ ] Définir le `ProductExtractionSchema` (Pydantic) :
    - Nom, Prix (actuel/ancien), Image, URL.
    - Specs techniques (Dictionnaire).
    - Note, Nombre d'avis, Résumé des avis (Points forts/faibles).
  - [ ] Implémenter `LLMExtractionStrategy` avec `gpt-4o-mini`.
  - [ ] Calculer le `trust_score` : `(Note * 0.7) + (log10(Avis) * 0.3)`.

### [PBI-103] Génération du Catalogue Markdown
- **Tâches** :
  - [ ] Créer les fichiers `.md` dans `data/raw/markdown/informatique/`.
  - [ ] Structure : Frontmatter YAML (données structurées) + Corps (Description texte).

## 🛠️ SPÉCIFICATIONS TECHNIQUES
- **Tool** : Crawl4AI (AsyncWebCrawler).
- **Model** : GPT-4o-mini (Extraction).
- **Format** : Markdown LLM-Ready.

## ✅ DEFINITION OF DONE (DoD)
- ~400 fichiers Markdown générés avec un Frontmatter complet.
- Présence du `trust_score` pour chaque produit.
- Structure de dossiers respectée.
