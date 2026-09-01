@echo off
rem Kas valanda pasiima naujas kainas is svetaines.
setlocal
title Kainu atnaujinimas
cd /d "%~dp0.."

set "PROFILE=%~1"
if "%PROFILE%"=="" set "PROFILE=profiles\sleepingexpert.json"

set "PY="
where python >nul 2>&1 && set "PY=python"
if not defined PY (
  where py >nul 2>&1 && set "PY=py -3"
)
if not defined PY exit /b 1

:loop
timeout /t 3600 /nobreak >nul
%PY% fetch_products.py --config "%PROFILE%" >nul 2>&1
goto loop
