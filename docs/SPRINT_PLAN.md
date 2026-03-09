# 🏃 SPRINT PLAN - SPRINT 13 : "THE COCKPIT & THE SHIELD"

**Objectif du Sprint** : Assainir le code en retirant les composants obsolètes et mettre en place les deux piliers de l'efficacité RAG : l'**Observabilité** (Cockpit Phoenix) et l'**Audit de Fidélité** (Shield DeepEval).

---

## 📋 TICKETS SÉLECTIONNÉS

### [PBI-1002] TECH : Nettoyage & Retrait Context7 (Expert Advisor)
**Priorité** : CRITIQUE | **Estimation** : S
**User Story** : "En tant que Lead-Dev, je veux supprimer les appels à l'Expert Advisor (MCP) dans le moteur RAG pour me baser uniquement sur les descriptions Jumia."
**Critères d'Acceptation** :
- [ ] Suppression de l'import et de l'usage de `expert_advisor` dans `src/rag_engine.py`.
- [ ] Suppression physique du fichier `src/expert_advisor.py`.
- [ ] Suppression de la logique de `expert_node` dans la synthèse de réponse.
- [ ] Validation (via tests unitaires) que le flux RAG fonctionne sans ce composant.

### [PBI-1306] TECH : Observabilité & Tracing (Arize Phoenix)
**Priorité** : High | **Estimation** : S
**User Story** : "En tant que Lead-Dev, je veux visualiser le cheminement complet de mes requêtes RAG pour identifier les latences et les sources d'erreur."
**Critères d'Acceptation** :
- [ ] Ajout de `arize-phoenix` et `openinference-instrumentation-llama-index` au `requirements.txt`.
- [ ] Dashboard Phoenix accessible en local.
- [ ] Traces complètes (Retriever -> Synthesis) visibles pour chaque requête.

### [PBI-1301/1303] EVAL : Audit "Intégrité Technique" (DeepEval + Gold Dataset)
**Priorité** : High | **Estimation** : M
**User Story** : "En tant qu'expert, je veux un score scientifique de fidélité pour m'assurer que le bot ne ment jamais sur les specs techniques."
**Critères d'Acceptation** :
- [ ] Ajout de `deepeval` au `requirements.txt`.
- [ ] Intégration de DeepEval avec le `gold_dataset.json`.
- [ ] Rapport de **Faithfulness** (Fidélité) sur les produits.

---

## 🏛️ RAPPEL TECHNIQUE & BLOQUANTS
1. **⚠️ DÉPENDANCES** : Le premier acte du sprint doit être la mise à jour du `requirements.txt` avec `deepeval` et `arize-phoenix`.
2. **NETTOYAGE** : Le PBI-1002 est un prérequis pour éviter d'instrumenter du code (Expert Advisor) qui va être supprimé.
3. **Phoenix** : Dashboard temps réel (Le "Comment").
4. **DeepEval** : Validation scientifique (Le "Combien").
5. **Gold Dataset** : Source de vérité immuable.
