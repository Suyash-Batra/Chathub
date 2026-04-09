#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# This will now recreate django_content_type, auth_permission, 
# and django_session from scratch. 
# --fake-initial will skip your 'base_message' and 'base_room' 
# so you don't lose your actual chat data.
python manage.py migrate --fake-initial
