# Guide d'installation Windows (Ultra Simplifié)

Ce guide est fait pour les débutants complets. Suivez chaque étape !

---

## Étape 1 : Installer Python

Python est le langage de programmation qui fait tourner Legofy.

### 1.1 Télécharger Python

1. Ouvrez votre navigateur (Chrome, Firefox, Edge...)
2. Allez sur : **https://www.python.org/downloads/**
3. Cliquez sur le gros bouton jaune **"Download Python 3.x.x"**

![Download Python](https://www.python.org/static/img/python-logo.png)

### 1.2 Installer Python

1. Ouvrez le fichier téléchargé (python-3.x.x.exe)
2. **⚠️ TRÈS IMPORTANT** : Cochez la case **"Add Python to PATH"** en bas de la fenêtre
3. Cliquez sur **"Install Now"**
4. Attendez que l'installation se termine
5. Cliquez sur **"Close"**

✅ Python est installé !

---

## Étape 2 : Télécharger Legofy

### 2.1 Télécharger le projet

1. Allez sur la page GitHub du projet
2. Cliquez sur le bouton vert **"Code"**
3. Cliquez sur **"Download ZIP"**
4. Un fichier `legofy-main.zip` se télécharge

### 2.2 Extraire le ZIP

1. Allez dans votre dossier **Téléchargements**
2. Faites un **clic droit** sur `legofy-main.zip`
3. Cliquez sur **"Extraire tout..."** ou **"Extract All..."**
4. Choisissez un emplacement simple, par exemple : `C:\Legofy`
5. Cliquez sur **"Extraire"**

✅ Legofy est téléchargé !

---

## Étape 3 : Lancer Legofy

### Méthode facile (Recommandée)

1. Ouvrez le dossier où vous avez extrait Legofy
2. **Double-cliquez** sur le fichier `install_and_run.bat`
3. Une fenêtre noire s'ouvre - c'est normal !
4. Attendez quelques secondes...
5. Votre navigateur s'ouvre automatiquement avec Legofy !

### Si ça ne marche pas

Essayez la méthode manuelle ci-dessous.

---

## Méthode manuelle (si la méthode facile ne marche pas)

### Ouvrir l'invite de commandes

1. Appuyez sur les touches `Windows + R` en même temps
2. Tapez `cmd` et appuyez sur Entrée
3. Une fenêtre noire s'ouvre

### Naviguer vers le dossier Legofy

Tapez cette commande (adaptez le chemin si nécessaire) :
```
cd C:\Legofy\legofy-main
```
Appuyez sur Entrée.

### Installer les dépendances

Tapez :
```
pip install flask pillow numpy
```
Appuyez sur Entrée. Attendez que ça se termine.

### Lancer l'application

Tapez :
```
python app.py
```
Appuyez sur Entrée.

### Ouvrir dans le navigateur

1. Ouvrez votre navigateur (Chrome, Firefox, Edge...)
2. Dans la barre d'adresse, tapez : `http://localhost:5001`
3. Appuyez sur Entrée

✅ Legofy devrait s'afficher !

---

## Utilisation quotidienne

Une fois installé, pour relancer Legofy :

1. Ouvrez le dossier Legofy
2. Double-cliquez sur `run.bat`
3. Votre navigateur s'ouvre avec l'application

---

## Problèmes fréquents

### "Python n'est pas reconnu"

Vous avez oublié de cocher "Add Python to PATH" pendant l'installation.

**Solution** : Réinstallez Python en cochant bien cette case.

### "Le port 5001 est déjà utilisé"

Une autre application utilise ce port.

**Solution** : Fermez l'autre application ou redémarrez votre ordinateur.

### La page ne s'affiche pas

**Solution** :
1. Vérifiez que la fenêtre noire (invite de commandes) est toujours ouverte
2. Tapez manuellement `http://localhost:5001` dans votre navigateur

### Erreur "pip n'est pas reconnu"

**Solution** :
1. Désinstallez Python
2. Réinstallez-le en cochant "Add Python to PATH"

---

## Besoin d'aide ?

Créez une "Issue" sur GitHub avec votre problème et une capture d'écran de l'erreur.
