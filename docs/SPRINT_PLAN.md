# 🏃 SPRINT PLAN - SPRINT 2 (RÉFORME & PERFECTION DU CATALOGUE)

## 🎯 OBJECTIF
Transformer l'extraction brute en un catalogue **"RAG-Ready Multi-Catégorie"** avec des données normalisées, une logique de "Master Product" (groupement d'offres) et une extraction logistique multi-hubs.

## 📋 TÂCHES À RÉALISER

### [PBI-120] Architecture Multi-Catégorie & Markdown v2 (Perfection)
**Priorité** : High | **Estimation** : M
**User Story** : "En tant qu'Assistant, je veux un catalogue normalisé et extensible, afin de fournir des recommandations précises sur n'importe quel produit (Informatique, Cosmétique, Bricolage)."
**Critères d'Acceptation** :
- [ ] Créer un schéma `CategoryAgnosticProduct` (Pydantic) avec `core_metadata` et `category_specs`.
- [ ] Implémenter la normalisation LLM (ex: "8Go" -> 8 GB, "100ml" -> 100 ml).
- [ ] Ajouter l'analyse de sentiment par axe (Performance, Design, Autonomie, Prix).
- [ ] Calculer automatiquement le `value_for_money_score`.
- [ ] **Test de Validation** : Scraper 5 produits de catégories différentes (ex: 1 Laptop, 1 Smartphone, 1 Cosmétique, 1 Bricolage, 1 Électroménager) pour vérifier la structure v2.

### [PBI-130] Extraction Logistique Dynamique (Livraison)
**Priorité** : High | **Estimation** : M
**User Story** : "En tant que client Jumia, je veux connaître le coût total de livraison (Hubs + Zone 3), afin de choisir l'offre la plus rentable pour ma ville."
**Critères d'Acceptation** :
- [ ] Interaction JS (Crawl4AI) pour les 5 hubs (Casa, Rabat, Tanger, Marrakech, Agadir).
- [ ] Capture du tarif "Plafond" (Zone 3 - ex: Dakhla).
- [ ] Stockage structuré dans le YAML (`shipping_fees`).

## 🛠️ SPÉCIFICATIONS TECHNIQUES
- **Moteur** : Crawl4AI (AsyncWebCrawler) + JS Dropdown Manipulation.
- **Normalisation** : GPT-4o-mini (Extraction forcée par schéma).
- **Groupement** : Script de post-processing `merge_offers.py` pour grouper les produits par modèle identique.

## ✅ DEFINITION OF DONE (DoD)
- Le catalogue informatique est 100% migré vers le nouveau format v2.
- Validation : 5 produits témoins de catégories différentes (ex: 1 Laptop, 1 Smartphone, 1 Cosmétique, 1 Bricolage, 1 Électroménager) sont scrapés avec succès dans le nouveau format.
- Les scripts sont extensibles aux catégories cosmétiques/bricolage sans modification majeure du code.
- Chaque produit a une fiche YAML valide avec métadonnées de livraison.
