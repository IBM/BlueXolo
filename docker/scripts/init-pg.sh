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
  postgresql-setup initdb
fi
