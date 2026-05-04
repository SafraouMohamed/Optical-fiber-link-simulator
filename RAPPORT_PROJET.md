# Rapport de Projet
## Simulateur de Liaison Optique - Cours Prof. Faouzi BAHLOUL

---

## 1. Introduction

Ce projet est un simulateur de liaison optique développé dans le cadre du cours de **Prof. Faouzi BAHLOUL** à l'ENIT. L'objectif est de fournir un outil pédagogique pour analyser les liaisons optiques selon les critères du cours.

### 1.1 Objectifs
- Implémenter les formules du cours d'optique
- Permettre l'analyse théorique des liaisons optiques
- Vérifier la faisabilité d'une liaison
- Calculer la distance maximale (Lmax)
- Calculer le débit maximal

### 1.2 Structure du système
Le simulateur est basé sur le cours "Systèmes de Communication Optique" qui couvre:
- Les fibres optiques (types, caractéristiques)
- Les pertes dans les fibres
- La dispersion (chromatique, intermodale)
- Le bilan de liaison

---

## 2. Détails Techniques

### 2.1 Technologies utilisées
- **HTML/CSS/JavaScript** pour l'application web
- **Python (optionnel)** pour la version Streamlit

### 2.2 Formule du bilan de liaison

Selon le cours (page 20-22):

```
Budget Optique = Pe - Pmin

Atotale = Afibre + Aépissures + Aconnecteurs + Afresnel + ηc

Condition: Atotale ≤ Budget Optique

Lmax_att = (Pinj - Pmin - Aconnecteurs - Afresnel) / α
```

### 2.3 Modes de calcul

| Mode | Entrée | Sortie |
|------|--------|--------|
| Vérifier | Distance L | FONCTIONNELLE / NON FONCTIONNELLE |
| Calculer Lmax | Débit cible | Distance maximale |
| Calculer Débit | Distance L | Débit maximal |

### 2.4 Paramètres principaux

#### Émetteur
- Puissance émise: Pe (dBm)
- Longueur d'onde: λ (nm)
- Perte de couplage: ηc (dB)

#### Fibre
- Type: SMF (Monomode) / MMF (Multimode)
- Atténuation: α (dB/km)
- Dispersion: Dc (ps/nm·km)

#### Récepteur
- Sensibilité: Pmin (dBm)

#### Système
- Perte connecteur (dB)
- Perte épissure (dB)
- Longueur bobine (km)

---

## 3. Étapes de développement

### Phase 1: Initialisation
- Création de la structure du projet
- Configuration des fichiers de base

### Phase 2: Implémentation des fonctions
- Fonction calculerDelta(n1, n2)
- Fonction calculerNA(n1, n2)
- Calcul de Lmax_att et Lmax_disp
- Calcul du nombre de splices

### Phase 3: Interface utilisateur
- Création de l'interface HTML/CSS
- Ajout des champs d'entrée
- Implémentation des trois modes

### Phase 4: Tests et corrections
- Correction du calcul de Pinj (ηc doit être soustrait)
- Correction du calcul des splices
- Correction de l'affichage du mode (SMF/Multimode)
- Suppression du champ L dupliqué

### Phase 5: Publication GitHub
- Création du dépôt GitHub
- Upload de tous les fichiers
- Documentation complète

---

## 4. Tests effectués

### Test 1: Exercice du cours page 22-23

**Paramètres d'entrée:**
- Pe = 7 dBm (5 mW)
- ηc = 4 dB
- α = 4 dB/km
- Pmin = -47 dBm
- Débit = 106 Mbps

**Résultats attendus:**
- Lmax ≈ 10-12 km
- Limité par atténuation

**Résultats obtenus:**
- Lmax = 12.0 km ✓

### Test 2: Vérificateur SMF à 11 km

**Paramètres:**
- Pe = 0 dBm
- ηc = 3 dB
- α = 0.2 dB/km
- L = 11 km
- Pmin = -30 dBm

**Résultats:**
- ✓ FONCTIONNELLE
- Marge = 20.4 dB

---

## 5. Bugs corrigés

| Bug | Description | Correction |
|-----|-------------|-------------|
| 1 | ηc ajouté au lieu d'être soustrait | Pinj = Pe - ηc |
| 2 | Trop de splices (436) | Calcul corrigé: floor(L/Lbobine) |
| 3 | Double champ L | Suppression du champ L dans Fibre |
| 4 | SMF affiche Multimode | Mode = "Monomode" for SMF |

---

## 6. Structure finale du projet

```
optical_simulator/
├── index.html          # Application principale
├── app.py             # Version Python Streamlit
├── requirements.txt   # Dépendances Python
├── README.md         # Documentation
├── data/
│   └── presets.json  # Préréglages
└── modules/          # Modules Python
    ├── __init__.py
    ├── emetteur.py
    ├── fibre.py
    ├── recepteur.py
    ├── bilan_liaison.py
    ├── analyse_modale.py
    └── sellmeier.py
```

---

## 7. Utilisation

### Pour les étudiants
1. Télécharger `index.html`
2. L'ouvrir dans un navigateur
3. Entrer les paramètres
4. Cliquer "Analyser"

### Pour le professeur
```bash
# Option Python
pip install -r requirements.txt
streamlit run app.py
```

---

## 8. Conclusion

Ce projet implémente faithfully les formules du cours de Prof. Faouzi BAHLOUL. Il permet aux étudiants de:
- Vérifier la faisabilité d'une liaison optique
- Calculer la distance maximale
- Comprendre l'impact des différents paramètres

Le code est disponible sur GitHub et peut être utilisé librement à des fins éducatives.

---

## 9. Informations

- **Auteur:** Développé dans le cadre du cours ENIT
- **Professeur:** Prof. Faouzi BAHLOUL
- **Université:** ENIT (École Nationale d'Ingénieurs de Tunis)
- **Année:** 2025-2026
- **Licence:** Usage éducatif

---

**Dépôt GitHub:**
https://github.com/SafraouMohamed/Optical-fiber-link-simulator