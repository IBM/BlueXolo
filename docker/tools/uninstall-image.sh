#!/bin/bash - 
##################################################
## (C) COPYRIGHT IBM Corp. 2018
##################################################
#  Description:  Uninstall Bluexolo Image from Docker
#
#       Author:  Fernando Quintero (fqa), quintero@mx1.ibm.com
#      VERSION:  1.0
#      Created:  09/19/18 09:07
#     Revision:  ---
##################################################
#

docker kill  $(docker ps -q)
docker rmi $(docker images bluexolo -q)
