#!/bin/bash - 
##################################################
## (C) COPYRIGHT IBM Corp. 2018
##################################################
#  Description:  
#
#       Author:  Fernando Quintero (fqa), quintero@mx1.ibm.com
#      VERSION:  1.0
#      Created:  04/02/2019 20:10
#     Revision:  ---
##################################################
#

#set -o nounset  # Treat unset variables as an error

# Kill BlueXolo and BlueXoloAssistant running containers
docker kill bluexolo bluexolo_assistant

# Remove network for offline virtual assistance
docker network rm offline_assistant

exit 0


