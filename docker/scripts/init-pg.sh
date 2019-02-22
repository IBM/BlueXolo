#!/bin/bash -
##################################################
## (C) COPYRIGHT IBM Corp. 2018
##################################################
#  Description:  initialize postgresql
#
#       Author:  Fernando Quintero (fqa), quintero@mx1.ibm.com
#      VERSION:  1.0
#      Created:  08/24/18 10:13
#     Revision:  ---
##################################################
#

if [ -e /FIRST_SETUP ]; then
echo "First setup..."
  if [ ! -e /var/lib/pgsql/data ]; then
    echo "Postgres data dir does not exist, initializing"
    mkdir -p /var/lib/pgsql/data
    chown -R postgres: /var/lib/pgsql
  fi
  postgresql-setup initdb
  systemctl restart postgresql
  if [ ! -e /var/lib/pgsql/BLUEXOLO ]; then
    echo "Setting up BlueXolo Data"
    su -l postgres -c  "psql < /update_pg_pwd.sql"
    sed -i -e '{s/ident/md5/g}' /var/lib/pgsql/data/pg_hba.conf
    sed -i -e '{s/peer/md5/g}' /var/lib/pgsql/data/pg_hba.conf
    systemctl restart postgresql
    su -l postgres -c "PGPASSWORD=bluexolo psql < /create_bluexolo_db.sql"
    touch /var/lib/pgsql/BLUEXOLO
  fi
fi
