# 🏃 SPRINT PLAN - SPRINT 18 : "HYGIÈNE & STABILITÉ"

**Objectif du Sprint** : Optimiser la pertinence des réponses en introduisant une mémoire éphémère (Session TTL) et stabiliser le socle technique en résolvant la dette accumulée.

---

## 📋 TICKETS SÉLECTIONNÉS

### [PBI-1801] TECH : Session TTL (Mémoire Éphémère & Hygiène)
**Priorité** : High | **Estimation** : M

**User Story** : "En tant qu'utilisateur, je veux que le bot oublie nos anciennes discussions après une période d'inactivité (30 min), afin de repartir sur un besoin frais sans confusion."

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Expiration de session**
  - **GIVEN** Une discussion active datant de plus de 30 minutes.
  - **WHEN** L'utilisateur envoie un nouveau message.
  - **THEN** Le `SimpleChatStore` vide l'historique précédent pour ce numéro.
- [ ] **Scenario 2 : Maintien du Persona**
  - **GIVEN** Un reset de session.
  - **WHEN** Le bot répond.
  - **THEN** Il conserve son ton Darija et ses instructions système malgré l'oubli du contenu.

### [PBI-1802] TECH : Résolution Dette Technique (Type Error)
**Priorité** : High | **Estimation** : S

**User Story** : "En tant que Lead-Dev, je veux corriger l'erreur de type sur `RESPONSE_TYPE` pour garantir la stabilité du moteur de chat."

**Critères d'Acceptation** :
- [ ] **Scenario 1 : Correction Type LlamaIndex**
  - **GIVEN** Le fichier `src/rag_engine.py`.
  - **WHEN** L'agent utilise `ContextChatEngine`.
  - **THEN** La signature de fonction supporte `Response | StreamingResponse | AsyncStreamingResponse` sans erreur de type.

### [PBI-1803] EVAL : Audit Qualité "Sawt Jumia" (Sprint 17 Logs)
**Priorité** : Medium | **Estimation** : S

**User Story** : "En tant que PO, je veux analyser les premiers logs réels du Sprint 17 pour vérifier si la prosodie Darija est bien acceptée par les utilisateurs."

**Critères d'Acceptation** :
- [ ] **Scenario 1 : Analyse de pertinence**
  - **GIVEN** 20 logs de conversations réelles (Vocal/Multimodal).
  - **WHEN** Passés dans le framework DeepEval.
  - **THEN** Le score d'Answer Relevancy doit être > 0.7.

---

## 🏛️ RAPPEL TECHNIQUE & BLOQUANTS
1. **DÉSÉQUILIBRE QDRANT** : Vérifier si la correction du type error résout les instabilités avant d'attaquer la mise à jour serveur Qdrant.
2. **TOKEN OPTIMIZATION** : La session TTL va naturellement réduire la taille du contexte envoyé au LLM, surveiller la baisse des coûts sur Phoenix.
