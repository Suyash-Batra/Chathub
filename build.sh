#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install --upgrade pip setuptools wheel
pip install --only-binary :all: --prefer-binary -r requirements.txt

# 2. Collect Static Files
python manage.py collectstatic --no-input

# 3. Apply Database Migrations with Safety Valve
# --fake-initial: If a table exists, Django marks it as "migrated" instead of crashing.
python manage.py migrate --fake-initial
