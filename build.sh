#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install --upgrade pip setuptools wheel
pip install --only-binary :all: --prefer-binary -r requirements.txt

# 2. Collect Static Files
python manage.py collectstatic --no-input

# 3. THE FORCE SYNC
# We use --fake-initial. 
# It creates missing tables (like django_session) 
# but ignores tables that already exist (like django_celery_beat).
python manage.py migrate --fake-initial
