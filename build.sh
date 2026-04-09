#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip setuptools wheel
pip install --only-binary :all: --prefer-binary -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
