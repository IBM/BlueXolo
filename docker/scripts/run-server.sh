
##################################################
## (C) COPYRIGHT IBM Corp. 2018
##################################################
#  Description:  Run Django Server
#
#       Author:  Fernando Quintero (fqa), quintero@mx1.ibm.com
#      VERSION:  1.0
#      Created:  08/25/18 20:43
#     Revision:  ---
##################################################
#

source /etc/bluexolo.env
cd $BLUEXOLO_DIR
nohup celery -A CTAFramework worker -l info &   # run celery
sleep 2                                         # take 2 secs
python3 manage.py runserver 0.0.0.0:8000 &      # run server
sleep 5                                         # take 5 secs
# --------------------------------------------
# if first time run set password for superuser
# --------------------------------------------
PGPASSWORD=bluexolo  psql < /users.sql 

