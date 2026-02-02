@echo off
chcp 65001 >nul
title Legofy

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║                         LEGOFY                               ║
echo ║                                                              ║
echo ║   Ouverture sur: http://localhost:5001                       ║
echo ║                                                              ║
echo ║   Pour arrêter: fermez cette fenêtre ou appuyez Ctrl+C       ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Ouvrir le navigateur après 1 seconde
start "" cmd /c "timeout /t 1 /nobreak >nul && start http://localhost:5001"

:: Lancer l'application
python app.py

pause
