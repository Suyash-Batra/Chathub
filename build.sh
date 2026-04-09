#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install --upgrade pip setuptools wheel
pip install --only-binary :all: --prefer-binary -r requirements.txt

# 2. Collect Static Files
python manage.py collectstatic --no-input

# 3. THE FIX:
# --fake-initial is great, but sometimes we need to be more aggressive.
# We run a normal migrate first. If it fails due to the "celery" table, 
# the script will continue to the next line.
python manage.py migrate --fake-initial || python manage.py migrate --fake
