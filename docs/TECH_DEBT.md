# 🏗️ DETTE TECHNIQUE & ALERTES

Ce fichier répertorie les points de vigilance techniques signalés par les agents ou le système.

## 🚨 ALERTES ACTIVES
- **[2026-03-16] Erreur de Type dans `src/rag_engine.py`** : 
    - **Localisation** : Ligne 200 environ.
    - **Problème** : `RESPONSE_TYPE` n'est pas compatible avec le type de retour `Response`. Probablement dû à l'utilisation de `AsyncStreamingResponse` non géré par la signature de fonction.
    - **Impact** : Risque de crash lors de l'intégration du `ContextChatEngine` (PBI-1001).
    - **Action demandée** : Correction prioritaire par le Lead-Dev.

## 📉 DETTE TECHNIQUE CUMULÉE
1. **Désynchronisation Qdrant** : (Noté au S13) Le client Qdrant 1.17 communique avec un serveur 1.10. Risque d'instabilité sur les filtres complexes.
2. **Gestion des Secrets** : Vérifier que `.env.example` contient bien toutes les clés nécessaires (Evolution API, OpenAI, Phoenix).
