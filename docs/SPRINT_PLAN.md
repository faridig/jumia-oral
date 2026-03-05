# 🏃 SPRINT PLAN - SPRINT 10
**Objectif** : Pivoter vers un moteur de recommandation Notebook pur et intentionnel.

## 📋 TICKET UNIQUE SÉLECTIONNÉ
### [PBI-2000] LE COMPAGNON NOTEBOOK (Pure Sémantique, Dual-Choice, Intent-based & Liens Directs)
**Priorité** : CRITIQUE | **Estimation** : L

**User Story** : 
"En tant que Personal Shopper Jumia, je veux comprendre l'intention d'usage de l'utilisateur pour lui proposer systématiquement les **deux meilleurs Notebooks** avec leurs **liens directs Jumia**, sans aucun biais de score, en me basant uniquement sur la pertinence technique."

**Critères d'Acceptation (DoR/DoD)** :
- [ ] **Action 1 : Nettoyage & Neutralité (RESET TOTAL)**
  - Retrait définitif du VFM, Trust Score et de la gestion de Localisation (villes).
  - **PURGE TOTALE** : Suppression physique de tous les fichiers `.md` existants dans `data/raw/markdown/notebooks/`.
  - **RESET QDRANT** : Suppression et recréation de la collection `jumia_products`.
- [ ] **Action 2 : Intelligence d'Usage**
  - Mappage des intentions (Gaming, Études, Montage) vers des filtres techniques CPU/RAM/GPU.
- [ ] **Action 3 : Structure "Top 2" & Liens**
  - Présentation obligatoire de 2 options avec : Nom, Prix, Specs clés et **URL cliquable Jumia**.
- [ ] **Action 4 : Diagnostic & "Full-Context Chunking"**
  - **DIAGNOSTIC CHUNKING** : Le Lead-Dev doit fournir un log montrant le découpage (Chunking) d'un fichier `.md` type.
  - **CONTRAINTE** : Bannir le découpage excessif. Viser **1 seul Chunk (Node) par produit** (si < 2000 tokens) pour garder l'unité de la fiche.
  - **INTÉGRITÉ** : **Aucune métadonnée ne doit être masquée au LLM** (`excluded_llm_metadata_keys` interdit). Le LLM doit avoir accès à 100% des specs et des URLs.
  - **INGESTION** : Scraping et ingestion de **30 articles Notebooks** maximum (Données 100% propres, sans scores).

**Responsable** : Lead-Dev

