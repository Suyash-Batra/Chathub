#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# THE FIX: 
# This tells Django to 'fake' the migrations that are already in the DB
# so it doesn't crash on 'already exists', but it WILL create 
# the missing 'django_session' table.
python manage.py migrate --fake-initial
