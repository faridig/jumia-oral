# 🏃 SPRINT PLAN - SPRINT 15 : "INTELLIGENCE STABLE"

**Objectif du Sprint** : Assurer la stabilité technique du moteur de chat et permettre la recherche par intention d'usage (ex: "PC pour étudiant") sans que l'utilisateur n'ait à connaître les specs techniques.

---

## 📋 TICKETS SÉLECTIONNÉS

### [PBI-1102] TECH/UX : Intelligence d'Intention & Stabilité (Usage Mapping)
**Priorité** : High | **Estimation** : M

**User Story** : "En tant que client non-expert, je veux exprimer mon besoin (ex: 'pour mes études') et que le bot identifie seul la RAM/CPU nécessaire, tout en profitant d'un système stable sans erreurs de type."

**Dépendances** : PBI-1001 (Mémoire Contextuelle)

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Correction de la Dette Technique (Context7 Best Practice)**
  - **GIVEN** Le fichier `src/rag_engine.py` présente une erreur de type sur `RESPONSE_TYPE`.
  - **WHEN** Le Lead-Dev utilise l'import correct `from llama_index.core.base.response.schema import RESPONSE_TYPE`.
  - **THEN** Le moteur de chat s'exécute sans avertissement de type.
- [ ] **Scenario 2 : Recherche par Intention Automatisée**
  - **GIVEN** Un utilisateur demande "Je cherche un laptop pour faire du montage vidéo".
  - **WHEN** Le `VectorIndexAutoRetriever` est sollicité avec un schéma `AttributeInfo` enrichi.
  - **THEN** Les logs Phoenix montrent une extraction correcte des filtres techniques (ex: `RAM >= 16`).
- [ ] **Scenario 3 : Fiabilité des Filtres Métadonnées**
  - **GIVEN** Un besoin métier (ex: Gaming).
  - **WHEN** Le LLM déduit les specs nécessaires.
  - **THEN** Le filtre `MetadataFilter` est appliqué avec l'opérateur `FilterOperator.GTE` ou `EQ` selon les cas, conformément à la documentation LlamaIndex.

---

## 🏛️ RAPPEL TECHNIQUE & BLOQUANTS
1. **STABILITÉ D'ABORD** : Le ticket ne peut être validé que si l'alerte de type dans `src/rag_engine.py` est levée.
2. **COÛT LLM** : L'étape de raisonnement pour l'intention consomme des tokens. Veiller à utiliser un prompt compact.
