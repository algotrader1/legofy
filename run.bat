@echo off
title Legofy

echo.
echo ========================================
echo              LEGOFY
echo ========================================
echo.
echo Ouvrez votre navigateur sur:
echo http://localhost:5001
echo.
echo Pour arreter: fermez cette fenetre
echo ========================================
echo.

timeout /t 2 /nobreak >nul
start http://localhost:5001

python app.py

pause
