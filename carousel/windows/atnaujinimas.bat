@echo off
rem Kas valanda pasiima naujas kainas is cookking.online.
chcp 65001 >nul
title Kainu atnaujinimas
cd /d "%~dp0.."
set PROFILE=%1
if "%PROFILE%"=="" set PROFILE=profiles\sleepingexpert.json
:loop
timeout /t 3600 /nobreak >nul
python fetch_products.py --config %PROFILE% >nul 2>&1
goto loop
