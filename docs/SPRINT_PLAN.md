# 🏃 SPRINT PLAN - SPRINT 9 (TEST & PIVOT PC)

## 🎯 OBJECTIF
Tester l'extraction spécialisée PC Portables sur un petit volume (10 produits) avant de réinitialiser complètement le catalogue.

## 📋 TÂCHES À RÉALISER

### [PBI-901] TECH : Purge & Reset (Clean Slate)
**Priorité** : High | **Estimation** : XS
**User Story** : "En tant que Lead-Dev, je veux vider les données obsolètes pour repartir sur un catalogue 100% PC Portables."
**Critères d'Acceptation** :
- [ ] Vider le dossier `data/` (fichiers `.md` et `.csv`).
- [ ] Supprimer et recréer la collection `jumia_products` dans Qdrant local.

### [SPIKE-902] TEST : Extraction Micro-Batch (10 Produits)
**Priorité** : High | **Estimation** : XS
**User Story** : "En tant que Chef d'Orchestre, je veux tester l'extraction LLM sur 10 produits pour valider la qualité des métadonnées."
**Critères d'Acceptation** :
- [ ] Lancer le crawler sur `https://www.jumia.ma/notebooks/`.
- [ ] **Limiter strictement à 10 produits**.
- [ ] Extraire les specs : CPU, RAM, SSD, GPU, Écran, État (Neuf/Renewed).
- [ ] Présenter le résultat JSON pour validation au Chef d'Orchestre.

### [PBI-903] INGESTION : Préparation de l'Index Laptop
**Priorité** : Medium | **Estimation** : XS
- Configurer les nouveaux champs de métadonnées dans l'Auto-Retriever.

## 🛠️ SPÉCIFICATIONS TECHNIQUES
- **URL** : `https://www.jumia.ma/notebooks/#catalog-listing`
- **Volume Test** : 10 produits.
- **Extraction LLM** : Forçage du schéma Pydantic spécialisé PC.

## ✅ DEFINITION OF DONE (DoD)
- Les 10 premiers PC sont extraits proprement avec leurs specs.
- Le Chef d'Orchestre a validé la structure des données.
- On est prêt pour le "Full Scale" (5 pages).
