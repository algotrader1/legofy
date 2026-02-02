@echo off
chcp 65001 >nul
title Legofy - Installation et démarrage

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║                    LEGOFY - Installation                     ║
echo ║                                                              ║
echo ║   Convertisseur d'images en motifs LEGO                      ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [1/3] Vérification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERREUR: Python n'est pas installé ou pas dans le PATH
    echo.
    echo Veuillez installer Python depuis: https://www.python.org/downloads/
    echo IMPORTANT: Cochez "Add Python to PATH" pendant l'installation!
    echo.
    pause
    exit /b 1
)
echo ✓ Python trouvé!
echo.

echo [2/3] Installation des dépendances...
pip install flask pillow numpy --quiet
if errorlevel 1 (
    echo.
    echo ❌ ERREUR lors de l'installation des dépendances
    echo Essayez de lancer ce script en tant qu'administrateur
    echo.
    pause
    exit /b 1
)
echo ✓ Dépendances installées!
echo.

echo [3/3] Démarrage de Legofy...
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   Legofy démarre sur: http://localhost:5001                  ║
echo ║                                                              ║
echo ║   Le navigateur va s'ouvrir automatiquement.                 ║
echo ║                                                              ║
echo ║   Pour arrêter: fermez cette fenêtre ou appuyez Ctrl+C       ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Ouvrir le navigateur après 2 secondes
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:5001"

:: Lancer l'application
python app.py

pause
