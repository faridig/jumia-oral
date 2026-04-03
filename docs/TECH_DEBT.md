# 🏗️ DETTE TECHNIQUE & ALERTES

Ce fichier répertorie les points de vigilance techniques signalés par les agents ou le système.

## 🚨 ALERTES ACTIVES
- *Aucune alerte active.*

## 📉 DETTE TECHNIQUE CUMULÉE
1. **Désynchronisation Qdrant** : (Noté au S13) Le client Qdrant 1.17 communique avec un serveur 1.10. Risque d'instabilité sur les filtres complexes.
2. **Gestion des Secrets** : Vérifier que `.env.example` contient bien toutes les clés nécessaires (Evolution API, OpenAI, Phoenix).

## ✅ DETTE RÉSOUDUE
- **[2026-03-31] Erreur de Type dans `src/rag_engine.py`** : Corrigée au Sprint 18 (PBI-1802). Signature de fonction désormais compatible avec `Response | StreamingResponse`.
