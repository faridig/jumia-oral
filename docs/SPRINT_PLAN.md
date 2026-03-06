# 🏃 SPRINT PLAN - SPRINT 11 : "GÉNÉRATION DU DATASET DE VÉRITÉ (GOLD DATASET)"

**Objectif du Sprint** : Créer un jeu de données de référence (Gold Dataset) basé sur les fiches produits réelles pour valider l'exactitude des informations techniques du bot.

---

### [PBI-1200] EVAL : Génération du Dataset Synthétique (Gold Dataset)
**Priorité** : High | **Estimation** : M
**Status** : READY 🚀

**User Story** : "En tant que Lead-Dev, je veux automatiser la création d'un dataset (Question/Contexte/Réponse attendue) pour m'assurer que le bot ne donne pas de fausses informations sur les laptops (ex: erreur de RAM ou de prix)."

**Dépendances** : Aucune (Se base sur les fichiers `.md` dans `data/raw/markdown/notebooks/`)

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Analyse des fichiers sources**
  - **GIVEN** Les 26 fiches produits Notebooks dans le dossier `data/`.
  - **WHEN** Le script de synthèse parcourt les fichiers.
  - **THEN** Il doit extraire les spécifications techniques (CPU, RAM, Prix) sans erreur de parsing.
- [ ] **Scenario 2 : Génération de Questions/Réponses (LLM Synth)**
  - **GIVEN** Une fiche produit spécifique (ex: HP EliteBook 840 G7).
  - **WHEN** On demande au LLM (GPT-4o-mini) de créer une question utilisateur réaliste.
  - **THEN** Il génère un couple `(Question, Ground_Truth)` basé strictement sur les données de la fiche.
- [ ] **Scenario 3 : Sortie JSON Structurée**
  - **GIVEN** L'exécution du script `scripts/generate_test_data.py`.
  - **WHEN** Le processus se termine.
  - **THEN** Un fichier `tests/gold_dataset.json` est créé contenant au moins 20 cas de test (Question, Context, Réponse attendue).

**Livrable Technique attendu** :
1. Un script `scripts/generate_test_data.py`.
2. Un fichier `tests/gold_dataset.json`.

---
*Note: Les autres PBI (Mémoire Contextuelle, Suppression ExpertAdvisor) sont repoussés au Sprint 12 pour garantir un focus total sur la qualité des données.*
