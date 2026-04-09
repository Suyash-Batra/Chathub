#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

python manage.py collectstatic --no-input

# 1. Force a "fake" reset of the migration state 
# This cleans up the mess from previous failed attempts
python manage.py migrate --fake base 0001 || true

# 2. Run the actual migration to create django_session and others
python manage.py migrate --fake-initial
