# Simulateur de Liaison Optique

Simulateur basé sur le cours de **Prof. Faouzi BAHLOUL** - ENIT

## Description

Application web pour analyser les liaisons optiques selon les critères:
- **Bilan de puissance** (attenuation, pertes)
- **Analyse de dispersion** (chromatique, intermodale)
- **Calcul de distance maximale** (Lmax)
- **Vérification de faisabilité** d'une liaison

## Utilisation

1. Ouvrir `index.html` dans un navigateur web
2. Entrer les paramètres du système optique
3. Cliquer sur **"Analyser"**

### Modes de calcul:

| Mode | Description |
|------|-------------|
| Vérifier | Vérifie si une distance L fonctionne |
| Calculer Lmax | Calcule la distance maximale pour un débit donné |
| Calculer Débit | Calcule le débit maximal pour une distance donnée |

## Paramètres principaux

### Émetteur
- Puissance émise Pe (dBm)
- Longueur d'onde λ (nm)
- Perte de couplage ηc (dB)

### Fibre
- Type: SMF (Monomode) / MMF (Multimode)
- Atténuation α (dB/km)
- Dispersion Dc (ps/nm·km)

### Récepteur
- Sensibilité Pmin (dBm)

### Système
- Perte connecteur (dB)
- Perte épissure (dB)
- Longueur bobine (km)

## Exemple d'exercice (Cours page 22-23)

| Paramètre | Valeur |
|----------|--------|
| Pe | 7 dBm (5 mW) |
| ηc | 4 dB |
| α | 4 dB/km |
| Pmin | -47 dBm |
| Bobine | 0.6 km |
| Débit | 106 Mbps |

**Résultat attendu:** Lmax ≈ 10-12 km

## Fichiers

```
optical_simulator/
├── index.html     # Application principale
└── modules/      # Modules Python (optionnel)
```

## Licence

Créé pour usage éducatif - Cours ENIT