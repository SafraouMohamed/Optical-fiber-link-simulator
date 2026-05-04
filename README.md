# Simulateur de Liaison Optique

Simulateur basé sur le cours de **Prof. Faouzi BAHLOUL** - ENIT

## Description

Application web pour analyser les liaisons optiques selon les critères:
- **Bilan de puissance** (attenuation, pertes)
- **Analyse de dispersion** (chromatique, intermodale)
- **Calcul de distance maximale** (Lmax)
- **Vérification de faisabilité** d'une liaison

## Comment l'utiliser

### Option 1 - Navigateur Web (Recommandé)

1. Télécharger le fichier `index.html`
2. L'ouvrir directement dans un navigateur web (Chrome, Firefox, Edge...)
3. C'est tout! Aucune installation nécessaire

### Option 2 - Python avec Streamlit

Si vous avez Python installé:

```bash
# Installez les dépendances
pip install -r requirements.txt

# Lancez l'application
streamlit run app.py
```

## Fonctionnalités

### Modes de calcul

| Mode | Description |
|------|-------------|
| **Vérifier** | Vérifie si une distance L donnée fonctionne |
| **Calculer Lmax** | Calcule la distance maximale pour un débit donné |
| **Calculer Débit** | Calcule le débit maximal pour une distance donnée |

### Paramètres d'entrée

#### Émetteur
- Puissance émise Pe (dBm)
- Longueur d'onde λ (nm)
- Largeur spectrale Δλ (nm)
- Perte de couplage ηc (dB)

#### Fibre
- Type: SMF (Monomode) / MMF (Multimode)
- Profil d'indice: Saut / Gradient (pour MMF)
- Indices de réfraction: cœur n1, gaine n2
- Rayon du cœur a (μm)
- Atténuation α (dB/km)
- Dispersion Dc (ps/nm·km)

#### Récepteur
- Sensibilité Pmin (dBm)

#### Système
- Mode de calcul
- Longueur L (km) - pour mode Vérifier
- Débit cible (Gbps) - pour mode Calculer Lmax
- Perte connecteur (dB)
- Perte épissure (dB)
- Longueur bobine (km)
- Adaptation d'indice: Oui/Non
- Codage: NRZ/RZ

## Exemple d'exercice (Cours page 22-23)

| Paramètre | Valeur |
|----------|--------|
| Pe | 7 dBm (5 mW) |
| ηc | 4 dB |
| α | 4 dB/km |
| Pmin | -47 dBm |
| Bobine | 0.6 km |
| Débit | 106 Mbps |

**Résultat attendu:** Lmax ≈ 10-12 km (limité par atténuation)

## Structure des fichiers

```
optical_simulator/
├── index.html          # Application web principale
├── app.py             # Application Streamlit (optionnel)
├── requirements.txt   # Dépendances Python
├── README.md          # Cette documentation
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

## À propos

- Créé pour usage éducatif dans le cadre du cours d'optique
- Prof. Faouzi BAHLOUL - ENIT
- Licence: Usage éducatif