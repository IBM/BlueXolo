#!/bin/bash

set -e

# Check for schema changes and apply them
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser and add variables to database
python3 run_base_migrations.py

# For robot control flow sentences
python3 manage.py initialize_robot

# Check the existance of all the required media directories
python3 manage.py check_media_dirs

if [ "$ENV_FILE" == "development" ]
then
    # Run (alternative to python3 manage.py runserver $DJANGO_IP:$DJANGO_PORT)
    gunicorn -c python:CTAFramework.gunicorn CTAFramework.wsgi:application
else
    # Enable uWSGI application
    uwsgi --socket :8000 --master --enable-threads --module CTAFramework.wsgi
fi