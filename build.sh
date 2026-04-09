#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies (Crucial step!)
pip install --upgrade pip setuptools wheel
pip install --only-binary :all: --prefer-binary -r requirements.txt

# 2. Collect Static Files
python manage.py collectstatic --no-input

# 3. Apply Database Migrations
python manage.py migrate
