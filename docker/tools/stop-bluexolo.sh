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

OPTION=$1

# Kill BlueXolo and BlueXoloAssistant running containers
docker kill bluexolo bluexolo_assistant

# Remove offline execution resources
if [ $OPTION == "--offline" ]
then
    docker kill language_server
    docker network rm offline_assistant
fi

exit 0


