#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# This will now see that django_migrations is gone and 
# try to create everything from scratch.
python manage.py migrate
