# 🏃 SPRINT PLAN - SPRINT 17 : "SAWT JUMIA + RICH MEDIA"

**Objectif du Sprint** : Orchestrer une réponse complète (Image + Texte/Liens + Vocal) pour une aide à l'achat immersive et professionnelle, en utilisant les dernières nouveautés OpenAI (TTS-mini) et LlamaIndex (Multimodal).

---

## 📋 TICKETS SÉLECTIONNÉS

### [PBI-1701.1] INFRA : Synthèse Vocale Ultra-Rapide (OpenAI TTS)
**Priorité** : High | **Estimation** : M

**User Story** : "En tant que Personal Shopper, je veux générer un audio de haute qualité en moins de 1s pour ne pas faire attendre l'utilisateur."

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Utilisation du modèle gpt-4o-mini-tts**
  - **GIVEN** Un texte de réponse en Darija.
  - **WHEN** Le système appelle l'API OpenAI TTS avec le modèle `gpt-4o-mini-tts`.
  - **THEN** Un fichier binaire `.opus` est généré avec succès.
- [ ] **Scenario 2 : Optimisation de la voix**
  - **GIVEN** Un besoin de tonalité marocaine chaleureuse.
  - **WHEN** La voix `marin` ou `cedar` est sélectionnée.
  - **THEN** La prononciation du Darija est fluide et naturelle.

### [PBI-1701.2] UX : Séquençage Multimédia & Orchestration
**Priorité** : High | **Estimation** : L

**User Story** : "En tant qu'utilisateur, je veux voir l'image du PC, lire ses caractéristiques et entendre l'avis du bot dans un flux logique et structuré."

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Séquençage automatique**
  - **GIVEN** Une recommandation de produit validée.
  - **WHEN** Le moteur de réponse est déclenché.
  - **THEN** WhatsApp reçoit successivement : 1. L'image du produit, 2. Le texte avec lien Jumia, 3. Le message vocal.
- [ ] **Scenario 2 : Liens Jumia Cliquables**
  - **GIVEN** Un texte de réponse.
  - **WHEN** Il contient une URL Jumia Notebooks.
  - **THEN** Elle est formatée pour être immédiatement cliquable sur mobile.

### [PBI-1701.3] PROMPT : Double flux de sortie (Prosodie vs Structure)
**Priorité** : Medium | **Estimation** : S

**User Story** : "En tant que système, je veux générer un texte propre pour WhatsApp (avec puces/emojis) et un texte fluide pour le TTS (sans caractères techniques)."

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Séparation des sorties**
  - **GIVEN** Un résultat de recherche RAG.
  - **WHEN** Le LLM prépare la réponse.
  - **THEN** Il produit deux variables : `text_whatsapp` (riche) et `text_tts` (phonétique/oral).

### [PBI-1702] EVAL : Audit de l'expérience multimodale
**Priorité** : Medium | **Estimation** : XS

**Action** : Test manuel de bout en bout (Voix -> RAG -> Image + Texte + Vocal) pour valider l'absence de régression et la cohérence des liens/images.

---

## 🏛️ RAPPEL TECHNIQUE & BLOQUANTS
1. **FORMAT OPUS** : S'assurer qu'Evolution API accepte le stream binaire directement depuis OpenAI sans conversion disque.
2. **MULTIMODAL** : Utiliser `image_url` depuis les métadonnées Qdrant pour l'envoi WhatsApp.
