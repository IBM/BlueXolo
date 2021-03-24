#!/bin/bash

set -e
cd ..

# Check for schema changes and apply them
python3 manage.py makemigrations
python3 manage.py migrate

# Initialize robot
python3 manage.py initialize_robot

#

# Reset ID's to prevent duplications due legacy data in DB
python3 manage.py sqlsequencereset Products Servers Testings Users

# Run
python3 manage.py runserver $DJANGO_IP:$DJANGO_PORT