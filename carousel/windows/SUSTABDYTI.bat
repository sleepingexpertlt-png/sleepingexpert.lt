@echo off
setlocal
title Sustabdymas
taskkill /f /im chrome.exe >nul 2>&1
taskkill /f /im msedge.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1
echo.
echo   Ekranas sustabdytas.
echo.
timeout /t 3 /nobreak >nul
