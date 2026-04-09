@echo off
title ChatHub Developer Environment
color 0B

:: 1. Move to the directory where the script is located
cd /d "%~dp0"

echo --------------------------------------------------
echo [1/4] Activating Virtual Environment...
echo --------------------------------------------------
:: THE FIX: Use 'call' so the script continues
if exist .\env\Scripts\activate.bat (
    call .\env\Scripts\activate.bat
) else (
    echo [ERROR] env folder not found!
    pause
    exit
)

echo --------------------------------------------------
echo [2/4] Booting Redis inside WSL...
echo --------------------------------------------------
wsl sudo service redis-server start || echo Redis already running.

:: Use 'python' directly now that 'call' has activated the env
echo [3/4] Starting Background Services...
start "Celery Beat" /min python -m celery -A studybud beat -l info
start "Celery Worker" /min python -m celery -A studybud worker -l info --pool=solo

echo --------------------------------------------------
echo [4/4] Starting Daphne...
echo --------------------------------------------------
:: If this fails, run 'pip install daphne' while env is active
python -m daphne -p 8000 studybud.asgi:application

pause