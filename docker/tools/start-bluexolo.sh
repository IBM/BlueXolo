#!/bin/bash

# Font colors depending on situation
ERROR=`tput setaf 1`
SUCCESS=`tput setaf 2`
WARNING=`tput setaf 3`
DEFAULT=`tput sgr0`

# Variable to hold the recieved option
OPTION=$1

#---  FUNCTION  ----------------------------------------------------------------
#   NAME:  Show_Help()
#   DESCRIPTION: Display all available commands
#-------------------------------------------------------------------------------
Show_Help() {
    echo -e "\nOptions:\n"
    echo -e "\t--no-assistant       Disable the BlueXolo Assistant\n"
    echo -e "\t--offline            Run the BlueXolo assistant independant of internet connection\n"
}

#---  FUNCTION  ----------------------------------------------------------------
#   NAME:  Run_Assistant()
#   DESCRIPTION: Run the assistant depending on the command options
#-------------------------------------------------------------------------------
Run_Assistant() {
    if [ -z "$OPTION" ]
    then
        echo "Fetching latest version of BlueXolo Assistant . . ."
    	docker pull snvc00/bluexolo-assistant:beta
        echo "${SUCCESS}Starting BlueXolo Assistant . . .${DEFAULT}"
    	docker run --rm -d -p 3000:3000 --name bluexolo_assistant snvc00/bluexolo-assistant:beta
    elif [ $OPTION == "--no-assistant" ]
    then 
        echo "${WARNING}BlueXolo Assistant disabled.${DEFAULT}"
    elif [ $OPTION == "--offline" ]
    then 
        echo "Fetching latest version of BlueXolo Assistant Offline . . ."
    	docker pull snvc00/bluexolo-assistant:offline
        echo "${SUCCESS}Starting BlueXolo Assistant Offline . . .${DEFAULT}"
        docker network create offline_assistant
        docker run --rm -d --name language_server --network offline_assistant snvc00/bluexolo-assistant:offline
        docker run --rm -d -p 3000:3000 --name bluexolo_assistant --network offline_assistant snvc00/bluexolo-assistant:offline bash -c "/botpress/duckling -p 8080 & /botpress/bp"
    elif [ $OPTION == "--help" ]
    then
        Show_Help
        exit 0
    else
        echo "${ERROR}Option: $OPTION is not valid. ${DEFAULT}'See --help'"
        Show_Help
        exit 1
    fi
}

# Run BlueXolo Assistant
Run_Assistant OPTION

# Get required paths 

# From input (default)
read -p "BlueXolo repository path: " BLUEXOLO_DIR
read -p "BlueXolo data path: " BLUEXOLO_DATA

# To use defined paths comment the two lines above then uncomment and set
# the values down here
#BLUEXOLO_DIR=/your/bluexolo
#BLUEXOLO_DATA=/your/bluexolo-data

# Run BlueXolo 
echo "Fetching latest version of BlueXolo . . ."
docker pull bluexolo/bluexolo:latest
echo "${SUCCESS}Starting BlueXolo . . .${DEFAULT}"
docker run -d --privileged --rm \
-p 8000:8000 \
-h bluexolo \
-e container=docker \
-v /sys/fs/cgroup:/sys/fs/cgroup \
-v ${BLUEXOLO_DIR}:/opt/BlueXolo-src \
-v ${BLUEXOLO_DATA}:/var/lib/postgresql \
--name bluexolo \
bluexolo/bluexolo

# Configure bluexolo user and check required directories
echo "Running startup configurations . . .${DEFAULT}"
docker exec -ti bluexolo bash -c "sleep 5 && /opt/BlueXolo-src/tools/check_dirs.sh && /opt/BlueXolo-src/docker/scripts/config-user.sh"

exit 0
​
#-------------------------------------------------------------------------------
# End of script
#-------------------------------------------------------------------------------