# 🏃 SPRINT PLAN - SPRINT 13 : "THE COCKPIT & THE SHIELD"

**Objectif du Sprint** : Mettre en place les deux piliers de l'efficacité RAG : l'**Observabilité** (Cockpit Phoenix) pour voir ce qui se passe, et l'**Audit de Fidélité** (Shield DeepEval) pour garantir zéro hallucination.

---

## 📋 TICKETS SÉLECTIONNÉS

### [PBI-1306] TECH : Observabilité & Tracing (Arize Phoenix)
**Priorité** : CRITIQUE | **Estimation** : S
**User Story** : "En tant que Lead-Dev, je veux visualiser le cheminement complet de mes requêtes RAG pour identifier les latences et les sources d'erreur."
**Critères d'Acceptation** :
- [ ] Dashboard Phoenix accessible en local.
- [ ] Traces complètes (Retriever -> Synthesis) visibles pour chaque requête.
- [ ] Monitoring automatique des tokens et du coût.

### [PBI-1301/1303] EVAL : Audit "Intégrité Technique" (DeepEval + Gold Dataset)
**Priorité** : High | **Estimation** : M
**User Story** : "En tant qu'expert, je veux un score scientifique de fidélité pour m'assurer que le bot ne ment jamais sur les specs techniques."
**Critères d'Acceptation** :
- [ ] Intégration de DeepEval avec le `gold_dataset.json`.
- [ ] Rapport de **Faithfulness** (Fidélité) sur les 26 produits.
- [ ] Rapport d'**Answer Correctness** (Précision de la réponse).

---

## 🏛️ RAPPEL TECHNIQUE
- **Phoenix** : Dashboard temps réel (Le "Comment").
- **DeepEval** : Validation scientifique (Le "Combien").
- **Gold Dataset** : Source de vérité immuable.
