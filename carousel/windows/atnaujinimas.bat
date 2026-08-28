@echo off
rem Kas valanda pasiima naujas kainas is cookking.online.
chcp 65001 >nul
title CookKing - kainu atnaujinimas
cd /d "%~dp0.."
:loop
timeout /t 3600 /nobreak >nul
python fetch_products.py --config profiles\cookking.json >nul 2>&1
goto loop
