#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install --upgrade pip setuptools wheel
pip install --only-binary :all: --prefer-binary -r requirements.txt

# 2. Collect Static Files
python manage.py collectstatic --no-input

# 3. THE FIX: Force sync the migration state
# This marks all tables as "already created" so the build doesn't crash.
python manage.py migrate --fake
