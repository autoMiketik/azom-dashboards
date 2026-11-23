@echo off
setlocal
cd /d "%~dp0"
py -3 dashboard_controller.py --config controller.json
if errorlevel 1 pause
