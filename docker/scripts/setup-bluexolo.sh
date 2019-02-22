#!/bin/bash -
##################################################
## (C) COPYRIGHT IBM Corp. 2018
##################################################
#  Description:  setup bluexolo
#
#       Author:  Fernando Quintero (fqa), quintero@mx1.ibm.com
#      VERSION:  1.0
#      Created:  08/24/18 11:11
#     Revision:  ---
##################################################
#

if [ -e /FIRST_SETUP ]; then
    useradd -m bluexolo
    echo "bluexolo" | passwd --stdin bluexolo
    chown -R bluexolo:bluexolo /opt/BlueXolo
    rabbitmqctl add_user bluexolo
    rabbitmqctl add_vhost bluehost
    rabbitmqctl set_user_tags bluexolo bluetag
    rabbitmqctl set_permissions -p bluehost bluexolo ".*" ".*" ".*"
    cd /opt/BlueXolo
    python3 manage.py migrate
    python3 manage.py makemigrations
    python3 manage.py migrate
    rm -f /FIRST_SETUP
fi
