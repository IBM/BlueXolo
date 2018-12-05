#!/bin/bash -
##################################################
## (C) COPYRIGHT IBM Corp. 2018
##################################################
#  Description:  Initialization script
#
#       Author:  Fernando Quintero (fqa), quintero@mx1.ibm.com
#      VERSION:  1.0
#      Created:  08/23/18 11:05
#     Revision:  ---
##################################################
#

if [ -e /FIRST_SETUP ]; then
  nohup /usr/local/bin/init-pg.sh &
  sleep 3
  nohup /usr/local/bin/setup-bluexolo.sh &
  sleep 3
fi

{
  flock 3
  /usr/sbin/init 
} 3</tmp/lock2
