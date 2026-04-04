# 🏃 SPRINT PLAN - SPRINT 21 (DEVOPS & DX)

**Objectif du Sprint** : Simplifier le cycle de vie du projet avec un script de pilotage unifié (Control Panel) pour lancer, arrêter et surveiller tous les services (WhatsApp, FastAPI, Qdrant).

---

## 📋 TICKETS SÉLECTIONNÉS

### [PBI-2101] DX : Script de Pilotage Unifié (Control Panel)
**Priorité** : High | **Estimation** : S

**User Story** : "En tant que Chef d'Orchestre, je veux lancer et arrêter tous les services du projet (FastAPI, Qdrant, Evolution API, Ngrok) avec une seule commande simple, afin de gagner du temps et de la facilité."

**Dépendances** : Aucune (Post-Sprint 20)

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1 : Démarrage rapide**
  - **GIVEN** Tous les services sont éteints.
  - **WHEN** Je lance `./jumia.sh start`.
  - **THEN** Les conteneurs Qdrant et Evolution API démarrent, suivis du serveur FastAPI et du tunnel Ngrok.
  - **THEN** Le script récupère automatiquement la nouvelle URL Ngrok et met à jour `WEBHOOK_URL` dans le `.env` ET dans l'instance Evolution API (plus de configuration manuelle).
- [ ] **Scenario 2 : Arrêt propre**
  - **GIVEN** Les services sont actifs.
  - **WHEN** Je lance `./jumia.sh stop`.
  - **THEN** Tous les processus et conteneurs liés au projet sont stoppés proprement.
- [ ] **Scenario 3 : Monitoring**
  - **GIVEN** N'importe quel état.
  - **WHEN** Je lance `./jumia.sh status`.
  - **THEN** Le script affiche l'état (UP/DOWN) de chaque brique technologique.
