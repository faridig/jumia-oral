# 🏃 SPRINT PLAN - SPRINT 19 (ENGAGEMENT & VENTE)

**Le Sprint 18 est officiellement terminé.**

---

## 🎯 OBJECTIFS DU SPRINT 19
- **Conversion Élite** : Passer du "Dual Choice" à la **"Single Sniper Recommendation"** pour une prise de décision instantanée.
- **Vocal Persuasif** : Transformer l'audio Phoenix en un véritable outil de vente (Darija persuasif).
- **Fiabilité Réelle** : Vérifier la validité des liens Jumia en temps réel avant recommandation.
- **Robustesse Conversationnelle** : Tester et blinder le bot contre les provocations (Adversarial Tests).

---

## 📋 TICKETS SÉLECTIONNÉS

### [PBI-1901] TECH : Vérification Temps-Réel (Stock/Lien)
**Priorité** : High | **Estimation** : M
**User Story** : "En tant qu'utilisateur, je veux être sûr que le lien Jumia recommandé est toujours valide et le produit en stock."
**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Lien mort détecté**
  - **GIVEN** Le RAG sélectionne un produit dont l'URL renvoie un 404.
  - **WHEN** Le système effectue le check pre-flight.
  - **THEN** Le produit est ignoré et le suivant dans le top-k est sélectionné.

### [PBI-1902] PROMPT : Stratégie de Relance "Besoin d'aide ?"
**Priorité** : Medium | **Estimation** : S
**User Story** : "En tant que Personal Shopper, je veux relancer poliment l'utilisateur si la discussion est restée en suspens."
**Critères d'Acceptation** :
- [ ] Création d'un prompt de relance chaleureux en Darija.
- [ ] Logique de déclenchement (Optionnel pour ce sprint, focus sur le prompt).

### [PBI-1903] EVAL : Test de Robustesse "Adversarial Darija"
**Priorité** : High | **Estimation** : M
**User Story** : "En tant que PO, je veux m'assurer que le bot ne sort jamais de son rôle même s'il est provoqué."
**Critères d'Acceptation** :
- [ ] Ajout de 10 cas de tests "provocations/insultes" dans `gold_dataset.json`.
- [ ] Validation du maintien du Persona "Sales Professional" malgré le bruit.

### [PBI-1904] PROMPT : High-Conversion Sniper & Sales Audio
**Priorité** : CRITIQUE | **Estimation** : S
**User Story** : "En tant que vendeur Jumia, je veux que le bot ne propose qu'un seul produit avec un argumentaire vocal irrésistible."
**Critères d'Acceptation** :
- [ ] **Moteur RAG** : Limitation à 1 seule recommandation par réponse.
- [ ] **Flux [WHATSAPP]** : Focus sur l'unique lien.
- [ ] **Flux [TTS]** : Ton persuasif ("Had l-bi si madi", "Mat-tfeltouch").

---

## 🤝 HANDOFF
**PLANNING VALIDÉ. À TOI LEAD-DEV.**
