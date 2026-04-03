# 🏃 SPRINT PLAN - SPRINT 20 (AUDIO-FIRST & MINIMALISME)

**Le Sprint 19 est terminé.**

---

## 🎯 OBJECTIFS DU SPRINT 20
- **L'Expérience Unifiée** : Fusionner la force de l'Audio Phoenix avec un lien WhatsApp minimaliste.
- **Séquençage Narratif** : Envoyer l'**Audio en premier** pour conseiller, puis le **Lien en second** pour agir.
- **Suppression du Bruit Visuel** : Éliminer les listes à puces techniques du texte WhatsApp (Reportées dans l'audio).

---

## 📋 TICKETS SÉLECTIONNÉS

### [PBI-2001] TECH : Réorganisation du Séquençage WhatsApp
**Priorité** : High | **Estimation** : S
**User Story** : "En tant qu'utilisateur, je veux d'abord entendre mon conseiller me parler en Darija avant de voir le lien technique."
**Critères d'Acceptation** :
- [ ] Inverser l'ordre d'envoi dans `src/session_manager.py` : Audio Phoenix -> Texte/Lien.
- [ ] Vérifier que la latence de génération TTS ne bloque pas l'expérience.

### [PBI-2002] PROMPT : Refonte "Sniper Minimaliste" (Link-Only)
**Priorité** : CRITIQUE | **Estimation** : S
**User Story** : "En tant que vendeur Jumia, je veux que mon message texte ne contienne que l'essentiel (Nom, Prix, Lien) pour faciliter l'achat."
**Critères d'Acceptation** :
- [ ] Suppression des listes à puces techniques dans le bloc `[WHATSAPP]`.
- [ ] Formatage cible : `*NOM DU PRODUIT* - *PRIX* MAD \n\n Khoudou mn hna : [URL]`.

### [PBI-2003] UX : Audio Phoenix "Vendeur Expert"
**Priorité** : High | **Estimation** : M
**User Story** : "En tant qu'acheteur, je veux que l'audio soit si riche et convaincant qu'il remplace avantageusement la fiche technique textuelle."
**Critères d'Acceptation** :
- [ ] Intégration fluide des specs (CPU, RAM, SSD) dans la narration Darija.
- [ ] Utilisation de métaphores de performance ("Madi", "Tayra", "Naddi").

---

## 🤝 HANDOFF
**PLANNING VALIDÉ. À TOI LEAD-DEV.**
