#!/bin/bash - 
##################################################
## (C) COPYRIGHT IBM Corp. 2018
##################################################
#  Description:  install robot and libraries
#
#       Author:  Fernando Quintero (fqa), quintero@mx1.ibm.com
#      VERSION:  1.0
#      Created:  12/04/2018 14:27
#     Revision:  ---
##################################################
#

#set -o nounset  # Treat unset variables as an error




pip3 install robotframework 
pip3 search robotframework | grep library | cut -d ' ' -f 1 | grep robotframework > /tmp/salida ;  for j in $(cat /tmp/salida); do  pip3 install $j;  done 
rm /tmp/salida
exit 0
