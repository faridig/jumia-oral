# 🏃 SPRINT PLAN - SPRINT 11 : "MESURE & QUALITÉ"

**Objectif du Sprint** : Mettre en place un système de mesure automatisé (RAG Triad) pour garantir l'exactitude des informations techniques et de la pertinence des recommandations.

---

### [PBI-1200] EVAL : Implémentation du RAG Triad (DeepEval)
**Priorité** : High | **Estimation** : M

**User Story** : "En tant que Lead-Dev, je veux automatiser l'évaluation de la pertinence pour m'assurer que le bot ne donne pas de fausses informations techniques."
**Dépendances** : Aucune
**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Mesure de la Fidélité (Faithfulness)**
  - **GIVEN** Un dataset de test avec questions et contextes Jumia.
  - **WHEN** On lance l'évaluation via DeepEval.
  - **THEN** Le score de Faithfulness doit identifier toute spec technique (RAM, CPU) inventée par le LLM.
- [ ] **Scenario 2 : Dataset de Référence**
  - **GIVEN** Le besoin de répétabilité.
  - **WHEN** On crée `tests/eval_dataset.json`.
  - **THEN** Il doit contenir au moins 5 paires (Question, Contexte, Ground Truth) représentatives.
- [ ] **Scenario 3 : Rapport Automatisé**
  - **GIVEN** L'exécution du script `scripts/evaluate_rag.py`.
  - **WHEN** Le script se termine.
  - **THEN** Il affiche un tableau récapitulatif des scores par metric.

---

### [PBI-1004] TECH : Suppression totale du Trust Score
**Priorité** : Medium | **Estimation** : S
**User Story** : "En tant que Lead-Dev, je veux supprimer le Trust Score pour ne garder que la pertinence sémantique, afin que l'évaluation soit basée sur des données pures."
**Critères d'Acceptation** :
- [ ] Retrait de `trust_score` du moteur RAG et du prompt.
- [ ] Nettoyage des fichiers Markdown dans `data/`.

---

### [PBI-1003] TECH : Suppression totale du Score VFM
**Priorité** : Medium | **Estimation** : S
**User Story** : "En tant que Lead-Dev, je veux retirer le score VFM pour simplifier l'évaluation."
**Critères d'Acceptation** :
- [ ] Retrait du champ `value_for_money_score` du code et de l'extraction.
