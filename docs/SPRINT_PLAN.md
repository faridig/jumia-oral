# 🏃 SPRINT PLAN - SPRINT 8 (WHATSAPP LIVE)

## 🎯 OBJECTIF
Permettre au Chef d'Orchestre de tester le moteur RAG directement sur son téléphone via WhatsApp.

## 📋 TÂCHES À RÉALISER

### [PBI-801] SETUP : Appairage WhatsApp (QR Code)
**Priorité** : High | **Estimation** : S
**User Story** : "En tant que Chef d'Orchestre, je veux scanner un QR Code pour connecter mon numéro WhatsApp au moteur RAG."
**Critères d'Acceptation** :
- [ ] Créer l'instance `Jumia-Oral-Agent` via `POST /instance/create` avec `integration: "WHATSAPP-BAILEYS"` et `qrcode: true`.
- [ ] Afficher le QR Code (Base64) ou fournir le lien pour le scanner.
- [ ] Valider la connexion via `CONNECTION_UPDATE`.

### [PBI-802] TECH : Exposition du Webhook (Tunneling)
**Priorité** : High | **Estimation** : S
**User Story** : "En tant que système, je veux une URL publique pour recevoir les messages WhatsApp en temps réel."
**Critères d'Acceptation** :
- [ ] Lancer un tunnel Ngrok ou LocalTunnel vers le port `8000` (FastAPI).
- [ ] Configurer l'URL du webhook dans Evolution API via `POST /webhook/set/Jumia-Oral-Agent`.
- [ ] Souscrire aux événements : `MESSAGES_UPSERT`, `CONNECTION_UPDATE`, `QRCODE_UPDATED`.

### [PBI-803] TECH : Récepteur Webhook FastAPI (Performance)
**Priorité** : High | **Estimation** : M
**User Story** : "En tant qu'utilisateur, je veux que le bot réponde sans délai technique (Timeout WhatsApp)."
**Critères d'Acceptation** :
- [ ] Créer l'endpoint `/webhook` dans FastAPI.
- [ ] Vérifier le `apikey` dans les headers pour sécuriser la réception.
- [ ] Utiliser `BackgroundTasks` pour déléguer la logique RAG et répondre immédiatement `200 OK` à Evolution API.
- [ ] Traiter les messages entrants (`MESSAGES_UPSERT`) : extraire le texte et l'ID de l'expéditeur.

### [PBI-804] UX : Test Live "Mrehba"
**Priorité** : Medium | **Estimation** : XS
**User Story** : "En tant qu'utilisateur, je veux recevoir un accueil en Darija dès mon premier message."
**Critères d'Acceptation** :
- [ ] Réussir un cycle complet : Message Utilisateur -> Webhook -> RAG -> Réponse WhatsApp.
- [ ] Vérifier que les images produits (si trouvées) sont bien envoyées via `sendMedia`.

## 🛠️ SPÉCIFICATIONS TECHNIQUES
- **Fichiers à modifier** : `src/main.py` (FastAPI Webhook), `src/session_manager.py` (Intégration Evolution API).
- **Sécurité** : Ne jamais versionner l'URL Ngrok ou le `apikey`. Utiliser le `.env`.
- **Performance** : Temps de réponse webhook < 2 secondes (impératif).

## ✅ DEFINITION OF DONE (DoD)
- Le Chef d'Orchestre peut converser avec son bot sur WhatsApp.
- Les logs montrent une réception propre des webhooks.
- Pas de blocage du serveur FastAPI pendant le traitement RAG (BackgroundTasks).
