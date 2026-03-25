# 🏃 SPRINT PLAN - SPRINT 16 : "SAWT EL BLED" (VOIX DU PAYS)

**Objectif du Sprint** : Intégrer l'interaction vocale en Darija via l'API OpenAI Whisper et assurer des réponses textuelles natives (sans traduction) pour une expérience utilisateur marocaine authentique.

---

## 📋 TICKETS SÉLECTIONNÉS

### [PBI-1103.1] INFRA : Intégration API OpenAI Whisper
**Priorité** : High | **Estimation** : M

**User Story** : "En tant qu'utilisateur, je veux envoyer un message vocal en Darija sur WhatsApp et que le bot comprenne exactement ma demande technique."

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Transcription de base**
  - **GIVEN** Un fichier audio .ogg reçu via Evolution API.
  - **WHEN** Le système appelle l'endpoint `v1/audio/transcriptions` d'OpenAI.
  - **THEN** Le texte retourné correspond fidèlement au Darija parlé.
- [ ] **Scenario 2 : Optimisation Dialectale**
  - **GIVEN** Une requête audio complexe avec des termes techniques.
  - **WHEN** L'API Whisper est appelée avec un `initial_prompt` spécifique au Darija/PC Jumia.
  - **THEN** Les termes comme "ra9a" ou "tayra" sont correctement transcrits.

### [PBI-1103.2] PROMPT : Moteur de Réponse Darija-Native (GPT-4o)
**Priorité** : High | **Estimation** : M

**User Story** : "En tant qu'utilisateur, je veux recevoir une réponse en Darija naturel, respectant mes codes culturels, sans sentir que c'est une traduction du français."

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Pensée Native**
  - **GIVEN** Une question transcrite en Darija.
  - **WHEN** Le LLM génère sa réponse.
  - **THEN** La structure grammaticale est celle du Darija (et non du Fusha ou du Français traduit).
- [ ] **Scenario 2 : Glossaire "Darija-Tech"**
  - **GIVEN** Une recommandation de PC.
  - **WHEN** Le bot décrit les performances.
  - **THEN** Il utilise les termes validés (ex: "madi" pour rapide, "mkhyr" pour excellent).

### [PBI-1103.3] UX : Onboarding Audio & WhatsApp Flow
**Priorité** : Medium | **Estimation** : S

**User Story** : "En tant qu'utilisateur, je veux savoir que je peux parler au bot dès mon premier message."

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Invitation vocale**
  - **GIVEN** Le message de bienvenue "Mrehba".
  - **WHEN** L'utilisateur le reçoit.
  - **THEN** Une phrase explicite l'invite à envoyer des messages vocaux.

### [PBI-1601] TECH : Hygiène Infra - Sync Qdrant
**Priorité** : Medium | **Estimation** : XS

**Action** : Aligner la version du client `qdrant-client` dans `requirements.txt` avec la version serveur (1.10) pour lever l'alerte de la dette technique.

---

## 🏛️ RAPPEL TECHNIQUE & BLOQUANTS
1. **TIMEOUT WHATSAPP** : La transcription Whisper ajoute de la latence. Utiliser impérativement les `BackgroundTasks` de FastAPI pour ne pas bloquer Evolution API.
2. **COÛTS** : Monitorer la consommation Whisper via Phoenix.
