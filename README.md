# Legofy 🧱

**Convertisseur d'images en motifs LEGO pour moules de sérigraphie**

Transformez n'importe quelle image en un patron de tuiles LEGO pour créer des moules de sérigraphie.

![Screenshot](docs/screenshot.png)

---

## ✨ Fonctionnalités

- 📷 **Import d'images** (PNG, JPG, etc.)
- 🎚️ **Seuil ajustable** avec aperçu en temps réel
- 📐 **Taille de grille personnalisable**
- 🧱 **Large choix de tuiles LEGO** avec références officielles
- 🔄 **Tuiles courbées Macaroni** pour les angles arrondis
- 📊 **Liste des pièces nécessaires** avec quantités
- 💾 **Export JSON** du plan de placement
- 🖼️ **Téléchargement de l'image** du résultat

---

## 🚀 Installation rapide (Windows)

### Méthode 1 : Installation en 3 clics (Recommandée)

1. **Téléchargez Python** : [python.org/downloads](https://www.python.org/downloads/)
   - ⚠️ **IMPORTANT** : Cochez ✅ "Add Python to PATH" pendant l'installation

2. **Téléchargez Legofy** : [Télécharger ZIP](https://github.com/algotrader1/legofy/archive/refs/heads/main.zip)
   - Extrayez le ZIP dans un dossier (ex: `C:\Legofy`)

3. **Double-cliquez sur `install_and_run.bat`**
   - L'application s'ouvre automatiquement dans votre navigateur !

### Méthode 2 : Installation manuelle

Voir le [Guide d'installation détaillé](docs/INSTALLATION_WINDOWS.md)

---

## 📖 Comment utiliser

1. **Chargez une image** (glissez-déposez ou cliquez)
2. **Ajustez le seuil** avec le slider pour définir le noir/blanc
3. **Réglez la taille de grille** (largeur × hauteur en studs LEGO)
4. **Sélectionnez les tuiles** que vous voulez utiliser
5. **Cliquez sur "Convertir"**
6. **Téléchargez** l'image résultat ou exportez en JSON

---

## 🧱 Tuiles LEGO supportées

### Tuiles rectangulaires
| Pièce | Référence |
|-------|-----------|
| Tuile 1×1 | #3070 |
| Tuile 1×2 | #3069 |
| Tuile 1×3 | #63864 |
| Tuile 1×4 | #2431 |
| Tuile 1×6 | #6636 |
| Tuile 1×8 | #4162 |
| Tuile 2×2 | #3068 |
| Tuile 2×3 | #26603 |
| Tuile 2×4 | #87079 |

### Tuiles Macaroni (quart de cercle)
| Pièce | Référence |
|-------|-----------|
| Macaroni 2×2 | #27925 |
| Macaroni 3×3 | #79393 |
| Macaroni 4×4 | #27507 |

### Tuiles rondes
| Pièce | Référence |
|-------|-----------|
| Ronde 1×1 | #98138 |
| Quart de rond 1×1 | #25269 |
| Demi-ronde 1×2 | #1126 |

---

## 🛠️ Pour les développeurs

### Prérequis
- Python 3.8+
- pip

### Installation
```bash
git clone https://github.com/algotrader1/legofy.git
cd legofy
pip install -r requirements.txt
python app.py
```

### Structure du projet
```
legofy/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── install_and_run.bat   # Script d'installation Windows
├── run.bat               # Script de lancement Windows
├── templates/
│   └── index.html        # Interface web
└── docs/
    └── INSTALLATION_WINDOWS.md
```

---

## 📝 Licence

MIT License - Libre d'utilisation et de modification.

---

## 🙏 Crédits

- Références LEGO via [Rebrickable](https://rebrickable.com) et [BrickLink](https://www.bricklink.com)
- Développé avec Flask et Pillow
