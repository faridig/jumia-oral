# 🏃 SPRINT PLAN - SPRINT 4 (RE-OPTIMISATION & TRANSPARENCE)

## 🎯 OBJECTIF
Améliorer la précision du moteur de recommandation en équilibrant les scores business/sémantiques et en renforçant la transparence sur les produits sans avis (Trust 0).

## 📋 TÂCHES À RÉALISER

### [PBI-401] TECH/UX : Équilibrage du Re-ranking (Poids Business vs Sémantique)
**Priorité** : High | **Estimation** : S
**User Story** : "En tant qu'utilisateur, je veux des résultats de recherche sémantiquement pertinents avant d'être commercialement performants, afin de ne pas voir de produits hors-sujet en tête de liste."
**Critères d'Acceptation** :
- [ ] Modifier la logique de pondération dans `JumiaReRanker`.
- [ ] Appliquer les nouveaux poids : **60% Sémantique / 40% Business** (Trust + VFM).
- [ ] **Test** : Vérifier que sur une requête "Crème visage", une cartouche d'encre (même bien notée) n'apparaît pas avant les produits de beauté.

### [PBI-402] PROMPT/SECURITY : Renforcement de la consigne d'Honnêteté (Trust Score 0)
**Priorité** : High | **Estimation** : XS
**User Story** : "En tant qu'utilisateur, je veux être explicitement averti lorsqu'un produit n'a pas encore d'avis, afin de prendre une décision d'achat éclairée et sécurisée."
**Critères d'Acceptation** :
- [ ] Injecter explicitement le `trust_score` dans les métadonnées textuelles envoyées au LLM.
- [ ] Mettre à jour le `System Prompt` pour forcer la mention du manque d'avis en Darija pour tout produit ayant un score de 0.
- [ ] **Test** : L'assistant doit répondre "Chouf, had l-produit ba9i madiyoroch fih l-avis" (ou similaire) lors de la présentation d'un produit neuf sans retour.

### [PBI-403] TECH : Affinage de l'Auto-Retriever (Over-filtering)
**Priorité** : Medium | **Estimation** : S
**User Story** : "En tant qu'utilisateur, je veux obtenir des résultats même si je ne précise pas de critères de qualité stricts, afin d'éviter les listes de résultats vides."
**Critères d'Acceptation** :
- [ ] Assouplir les descriptions de filtres dans `AutoRetriever`.
- [ ] Configurer le retriever pour qu'il ne filtre sur `trust_score` QUE si des termes comme "fiable", "bien noté" ou "avis" sont détectés.
- [ ] **Test** : Une requête simple "Laptop" doit retourner des résultats même si le trust_score est faible ou nul.

## 🛠️ SPÉCIFICATIONS TECHNIQUES
- **Fichiers concernés** : `core/rag/reranker.py`, `core/rag/retriever.py`, `prompts/system_prompt.txt`.
- **Validation** : Comparaison avant/après sur un set de 5 requêtes types (Ambiguë, Précise, Qualité, Prix).

## ✅ DEFINITION OF DONE (DoD)
- Les poids du re-ranking sont ajustés.
- Le LLM signale systématiquement les produits sans avis.
- L'Auto-Retriever ne vide plus les résultats par excès de zèle.
- Aucun secret ou clé API en dur dans les prompts.
