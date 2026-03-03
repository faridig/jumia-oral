# 🏃 SPRINT PLAN - SPRINT 7 (INFRA & CONNECTIVITÉ)

## 🎯 OBJECTIF
Établir la connexion réelle avec WhatsApp et préparer le terrain pour les supports multimédias.

## 📋 TÂCHES À RÉALISER

### [PBI-301] TECH : Mise en service de la Gateway WhatsApp
**Priorité** : High | **Estimation** : L
**User Story** : "En tant qu'utilisateur, je veux pouvoir envoyer un message sur un numéro WhatsApp et recevoir la réponse du moteur RAG."
**Critères d'Acceptation** :
- [ ] Lancement et configuration d'Evolution API via Docker.
- [ ] Création d'un endpoint FastAPI pour recevoir les Webhooks d'Evolution API.
- [ ] Test de bout en bout : Message WhatsApp -> RAG -> Réponse WhatsApp.

### [PBI-601] UX : Support des Images sur WhatsApp
**Priorité** : Medium | **Estimation** : M
**Note** : Dépend de la réussite du PBI-301.
**User Story** : "En tant qu'utilisateur, je veux voir la photo du produit recommandé."
**Critères d'Acceptation** :
- [ ] Extraire l'URL de l'image depuis les métadonnées.
- [ ] Implémenter la fonction `sendMedia` utilisant le SDK Evolution API.

### [PBI-602] TECH/UX : Comparaison de Panier Assistée
**Priorité** : Medium | **Estimation** : M
**User Story** : "En tant que client hésitant, je veux demander 'Lequel est le meilleur ?' pour obtenir un tableau comparatif technique et business entre les deux premiers produits du RAG."
**Critères d'Acceptation** :
- [ ] Détecter l'intention de comparaison dans la requête.
- [ ] Générer un tableau Markdown structuré (Specs, Trust Score, VFM).
- [ ] Ajouter une conclusion "Verdict de l'Expert" en Darija.

## 🛠️ SPÉCIFICATIONS TECHNIQUES
- **Fichiers concernés** : `src/session_manager.py` (pour l'envoi média), `src/rag_engine.py` (pour la logique de comparaison).
- **API** : Evolution API `/message/sendMedia`.

## ✅ DEFINITION OF DONE (DoD)
- Les images s'affichent correctement sur WhatsApp.
- Le tableau comparatif est lisible et utile.
- Pas de régression sur le ton de voix Darija.
