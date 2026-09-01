@echo off
chcp 65001 >nul
title Produktu ekranas
cd /d "%~dp0.."

rem ==== KLIENTAS: pakeisk sias dvi eilutes, jei naudoji kita parduotuve ====
set PROFILE=profiles\sleepingexpert.json
set DATA=data-se
rem =======================================================================

echo.
echo   ============================================
echo     SLEEPING EXPERT - produktu ekranas
echo   ============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo   [!] Nerastas Python.
  echo.
  echo   Idiek vienu paspaudimu is Microsoft Store:
  echo   atidaryk Store, ieskok "Python 3.12", spausk "Get".
  echo   Po to paleisk si faila is naujo.
  echo.
  pause
  exit /b 1
)

echo   [1/3] Siunciamos prekes is svetaines...
python fetch_products.py --config %PROFILE%
if errorlevel 1 (
  echo.
  echo   [!] Nepavyko atnaujinti. Rodomos paskutines issaugotos kainos.
  echo.
)

echo   [2/3] Paleidziamas ekranas...
start "Ekrano serveris" /min python serve.py --data %DATA% --port 8080
start "Kainu atnaujinimas" /min cmd /c "%~dp0atnaujinimas.bat" %PROFILE%

timeout /t 3 /nobreak >nul

echo   [3/3] Atidaroma naršykle...
set BROWSER=
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set BROWSER=%ProgramFiles%\Google\Chrome\Application\chrome.exe
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set BROWSER=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe
if not defined BROWSER if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" set BROWSER=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe
if not defined BROWSER if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" set BROWSER=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe

if defined BROWSER (
  start "" "%BROWSER%" --kiosk --start-fullscreen --disable-infobars --noerrdialogs --autoplay-policy=no-user-gesture-required "http://localhost:8080/"
) else (
  start "" "http://localhost:8080/"
)

echo.
echo   Veikia. Ekranas pats atsinaujins kas valanda.
echo.
echo   Isjungti: uzdaryk narsykle (Alt+F4) ir si langa.
echo.
timeout /t 8 /nobreak >nul
exit /b 0
