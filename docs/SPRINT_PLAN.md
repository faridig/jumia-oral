# 🏃 SPRINT PLAN - SPRINT 12 : Hygiène & Alignement Documentaire

**Objectif du Sprint** : Nettoyer le projet des traces de fonctionnalités obsolètes (Localisation, Trust Score) et mettre à jour la documentation pour refléter la vision "Compagnon Notebook" actuelle.

---

## 📋 TICKETS SÉLECTIONNÉS

### [PBI-1006] TECH/UX : Retrait de la gestion de Localisation
**Priorité** : High | **Estimation** : XS
**User Story** : "En tant que Lead-Dev, je veux supprimer le flux d'onboarding lié à la ville et toute mention de localisation dans les réponses, pour me concentrer exclusivement sur les produits."
**Critères d'Acceptation** :
- [ ] Suppression du flux de demande de ville dans `src/session_manager.py`.
- [ ] Retrait de la persistance de localisation dans le `SimpleChatStore`.
- [ ] Mise à jour du prompt système pour interdire toute mention de ville ou de logistique locale.

### [PBI-1201] DOC : Refonte du README.md (Alignement Vision Notebook)
**Priorité** : High | **Estimation** : S
**User Story** : "En tant qu'utilisateur, je veux un README à jour afin de comprendre la vision réelle du projet (Notebook Companion) sans être induit en erreur par d'anciennes fonctionnalités supprimées."
**Critères d'Acceptation** :
- [ ] Suppression des mentions Trust Score et VFM (obsolètes).
- [ ] Suppression des sections sur la Localisation (villes, livraison).
- [ ] Mise à jour de la Stack Technique (Crawl4AI, LlamaIndex Hybrid, Evolution API).
- [ ] Actualisation de l'état d'avancement et de la vision "Pure Sémantique".

### [PBI-1202] TECH : Nettoyage src/main.py (Alignement Démo)
**Priorité** : High | **Estimation** : XS
**User Story** : "En tant que développeur, je veux que le script de démo reflète le flux actuel du bot (sans localisation) pour éviter des erreurs d'exécution ou de compréhension."
**Critères d'Acceptation** :
- [ ] Retrait du message "Ana f Casablanca" et de la logique d'onboarding ville.
- [ ] Mise à jour des messages de test pour se concentrer sur la recherche de Notebooks.
- [ ] Mise à jour du print d'entête (Sprint 12).

---

## 🏛️ RAPPEL TECHNIQUE
- **Full-Context Node** : 1 produit = 1 chunk.
- **Top 2** : Toujours proposer deux options.
- **Zéro Localisation** : Plus de mentions de villes ou de logistique.
