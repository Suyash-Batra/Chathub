#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# This MUST run. If the build crashes before this, the 1146 error stays.
python manage.py migrate --fake-initial
