@echo off
title Legofy - Installation

echo.
echo ========================================
echo         LEGOFY - Installation
echo ========================================
echo.

echo [1/3] Verification de Python...
python --version
if errorlevel 1 (
    echo.
    echo ERREUR: Python n'est pas installe!
    echo.
    echo Installez Python depuis: https://www.python.org/downloads/
    echo IMPORTANT: Cochez "Add Python to PATH" pendant l'installation!
    echo.
    pause
    exit /b 1
)
echo OK - Python trouve!
echo.

echo [2/3] Installation des dependances...
echo Cela peut prendre 1-2 minutes...
python -m pip install flask pillow numpy
if errorlevel 1 (
    echo.
    echo ERREUR lors de l'installation
    echo Essayez: python -m pip install flask pillow numpy
    echo.
    pause
    exit /b 1
)
echo OK - Dependances installees!
echo.

echo [3/3] Demarrage de Legofy...
echo.
echo ========================================
echo   Legofy demarre sur: http://localhost:5001
echo.
echo   Ouvrez votre navigateur et allez sur:
echo   http://localhost:5001
echo.
echo   Pour arreter: fermez cette fenetre
echo ========================================
echo.

timeout /t 3 /nobreak >nul
start http://localhost:5001

python app.py

pause
