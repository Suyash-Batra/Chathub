#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip setuptools wheel
pip install --only-binary :all: --prefer-binary -r requirements.txt

python manage.py collectstatic --no-input

# 1. Fake the migrations first so Django thinks they are done
python manage.py migrate --fake

# 2. Run a real migrate just in case anything was actually missing
python manage.py migrate
