#!/bin/bash

set -e

PORT=${DJANGO_PORT:-8000}

# IMPORTANT: These commands are commented until the team define who
#            is going to run them and when.
# ------------------------------------------------------------------------
# Check for schema changes and apply them
#python3 manage.py makemigrations
#python3 manage.py migrate

# Add superuser
#python3 manage.py createsuperuser --email bluexolo@bluexolo.net --no-input

# Add variables to database
#python3 manage.py run_base_migrations.py

# For robot control flow sentences
#python3 manage.py initialize_robot

# Reset ID's to prevent duplications due legacy data in DB
#python3 manage.py sqlsequencereset Products Servers Testings Users
# ------------------------------------------------------------------------

# Run (alternative to python3 manage.py runserver $DJANGO_IP:$DJANGO_PORT)
GUNICORN_LOG_FILE=gunicorn_$(date +'%m_%d_%Y-%X').log
nohup gunicorn --bind :$PORT --workers 3 CTAFramework.wsgi:application > /var/www/logs/$GUNICORN_LOG_FILE &