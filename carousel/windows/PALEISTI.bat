@echo off
setlocal
title Produktu ekranas
cd /d "%~dp0.."

rem ==== KLIENTAS: pakeisk sias dvi eilutes, jei naudoji kita parduotuve ====
set "PROFILE=profiles\sleepingexpert.json"
set "DATA=data-se"
rem =======================================================================

echo.
echo   ============================================
echo     SLEEPING EXPERT - produktu ekranas
echo   ============================================
echo.

rem --- surandame Python (Store diegimas duoda "python", python.org duoda "py") ---
set "PY="
where python >nul 2>&1 && set "PY=python"
if not defined PY (
  where py >nul 2>&1 && set "PY=py -3"
)

if not defined PY (
  echo   [!] Nerastas Python.
  echo.
  echo   Idiek vienu paspaudimu:
  echo     1. Atidaryk Microsoft Store
  echo     2. Ieskok: Python 3.12
  echo     3. Spausk Get
  echo.
  echo   Po to paleisk si faila is naujo.
  echo.
  pause
  exit /b 1
)

echo   [1/3] Siunciamos prekes is svetaines...
%PY% fetch_products.py --config "%PROFILE%"
if errorlevel 1 (
  echo.
  echo   [!] Nepavyko atnaujinti kainu. Rodomos paskutines issaugotos.
  echo.
)

if not exist "%DATA%\products.json" (
  echo   [!] Truksta duomenu failo: %DATA%\products.json
  echo   Patikrink interneto rysi ir bandyk dar karta.
  echo.
  pause
  exit /b 2
)

echo   [2/3] Paleidziamas ekranas...
start "NEUZDARYTI - ekrano serveris" /min %PY% serve.py --data "%DATA%" --port 8080
start "NEUZDARYTI - kainu atnaujinimas" /min cmd /c call "%~dp0atnaujinimas.bat" "%PROFILE%"

timeout /t 3 /nobreak >nul

echo   [3/3] Atidaroma narsykle...
set "BROWSER="
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set "BROWSER=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
if not defined BROWSER if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set "BROWSER=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
if not defined BROWSER if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" set "BROWSER=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
if not defined BROWSER if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" set "BROWSER=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"

if defined BROWSER (
  start "" "%BROWSER%" --kiosk --start-fullscreen --disable-infobars --noerrdialogs "http://localhost:8080/"
) else (
  start "" "http://localhost:8080/"
)

echo.
echo   Veikia. Ekranas pats atsinaujins kas valanda.
echo.
echo   SVARBU: uzduociu juostoje liko du maziuliai langai,
echo   pavadinti "NEUZDARYTI ...". Jie turi likti atidaryti -
echo   vienas atiduoda ekrana, kitas siunia naujas kainas.
echo   Sitas langas uzsidarys pats, ji uzdaryti galima.
echo.
echo   Viska isjungti: SUSTABDYTI.bat
echo.
timeout /t 10 /nobreak >nul
exit /b 0
