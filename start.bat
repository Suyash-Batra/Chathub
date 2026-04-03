@echo off

echo Starting Daphne...
:: Redirecting output to nul prevents the creation of daphne.log
start /b daphne studybud.asgi:application > nul 2>&1

echo Starting Celery Worker...
:: Redirecting output to nul prevents the creation of worker.log
start /b celery -A studybud worker -l info -P eventlet > nul 2>&1

echo Starting Celery Beat...
:: Redirecting output to nul prevents the creation of beat.log
start /b celery -A studybud beat -l info > nul 2>&1

echo All services started (Logs disabled)...
pause