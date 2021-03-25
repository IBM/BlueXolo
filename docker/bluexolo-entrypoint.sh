#!/bin/bash

set -e

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
gunicorn -c python:CTAFramework.gunicorn CTAFramework.wsgi:application