@echo off
chcp 65001 >nul
title CookKing - sustabdymas
taskkill /f /im chrome.exe >nul 2>&1
taskkill /f /im msedge.exe >nul 2>&1
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo list ^| find "PID:"') do taskkill /f /pid %%i >nul 2>&1
echo   Sustabdyta.
timeout /t 3 /nobreak >nul
