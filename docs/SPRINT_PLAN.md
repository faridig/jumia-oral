# 🏃 SPRINT PLAN - SPRINT 5 (QUALITÉ & PERTINENCE)

## 🎯 OBJECTIF
Éliminer les faux positifs sémantiques en instaurant un seuil de similarité strict, garantissant que seuls les produits réellement pertinents sont proposés, quels que soient leurs scores business.

## 📋 TÂCHES À RÉALISER

### [PBI-404] TECH/UX : Seuil de Pertinence Sémantique (Hard-Filtering)
**Priorité** : High | **Estimation** : S
**User Story** : "En tant qu'utilisateur, je veux que les produits sémantiquement faibles (< 0.8) soient éliminés de la liste de re-ranking, même s'ils ont des scores business parfaits."
**Critères d'Acceptation** :
- [x] Définir un seuil de similarité vectorielle (ex: 0.8) dans le `JumiaReRanker`.
- [x] Tout produit en dessous du seuil doit être supprimé de la liste AVANT le calcul du boost business.
- [x] **Test** : Une requête "Crème" ne doit jamais retourner une "Cartouche d'encre" même si cette dernière a un Trust Score de 5.0.

## 🛠️ SPÉCIFICATIONS TECHNIQUES
- **Fichiers concernés** : `src/rag_engine.py` (Classe `JumiaReRanker`).
- **Logique** : Ajouter un filtre `node_with_score.score >= 0.8` au début de la méthode `_postprocess_nodes`.
- **Validation** : Test manuel avec la requête "Crème visage" et vérification de l'absence de produits informatiques.

## ✅ DEFINITION OF DONE (DoD)
- Le seuil de 0.8 est appliqué et fonctionnel.
- Les tests de non-régression sémantique sont validés.
- Aucun produit hors-sujet n'apparaît en tête de liste par simple "biais de confiance".
