#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install --upgrade pip setuptools wheel
pip install --only-binary :all: --prefer-binary -r requirements.txt

# 2. Collect Static Files
python manage.py collectstatic --no-input

# 3. FIX THE GHOST MIGRATIONS
# This tells Django to "forget" it faked the core apps so it can run them for real
python manage.py migrate sessions zero || true
python manage.py migrate auth zero || true

# 4. Now run them for real (No --fake flag!)
python manage.py migrate
