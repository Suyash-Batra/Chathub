web: gunicorn studybud.wsgi:application
worker: celery -A studybud worker --loglevel=info
beat: celery -A studybud beat --loglevel=info