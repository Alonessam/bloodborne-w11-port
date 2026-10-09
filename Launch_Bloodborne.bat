@echo off
title Bloodborne PC (Native Windows Port)
cd /d "%~dp0"
echo =======================================================
echo          Bloodborne PC - Native Windows Port
echo         High-Performance Vulkan 1.3 Translation
echo =======================================================
echo.
set BB_SAVE_LOG=1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\run.ps1" -SaveLog
echo.
echo =======================================================
echo Session ended. Press any key to close this window...
echo =======================================================
pause
