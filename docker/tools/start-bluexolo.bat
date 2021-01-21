@echo off

title Start BlueXolo
echo:

:: Variable to hold the recieved option
set OPTION=%1

:: Evaluate the received options
if [%OPTION%]==[] goto :run-assistant
if %OPTION%==--offline goto :run-assistant-offline
if %OPTION%==--no-assistant goto :not-run-assistant
if %OPTION%==--help goto :help

:: In case of not defined option, show help
echo BlueXolo: %OPTION% is not a valid option. 'See --help'
echo:

:: List available options and their description
:help
echo Options:
echo     --no-assistant       Disable the BlueXolo Assistant
echo     --offline            Run the BlueXolo assistant independent of internet connection
echo:
exit 0

:: Disable the BlueXolo Assistant
:not-run-assistant
echo BlueXolo Assistant disabled
goto :run-bluexolo

:: Run BlueXolo Assistant docker image independent of internet connection
:run-assistant-offline
echo Fetching latest version of BlueXolo Assistant Offline . . .
docker pull snvc00/bluexolo-assistant:offline
echo Starting BlueXolo Assistant Offline . . .
docker network create offline_assistant
docker run --rm -d --name language_server --network offline_assistant snvc00/bluexolo-assistant:offline
docker run --rm -d -p 3000:3000 --name bluexolo_assistant --network offline_assistant snvc00/bluexolo-assistant:offline bash -c "/botpress/duckling -p 8080 & /botpress/bp"

goto :run-bluexolo

:: Run BlueXolo Assistant default docker image
:run-assistant
echo Fetching latest version of BlueXolo Assistant . . .
docker pull snvc00/bluexolo-assistant:beta
echo Starting BlueXolo Assistant . . .
docker run --rm -d -p 3000:3000 --name bluexolo_assistant snvc00/bluexolo-assistant:beta
goto :run-bluexolo

:: Run BlueXolo
:run-bluexolo

:: Get required paths 

:: From input (default)
set /p BLUEXOLO_DIR=BlueXolo repository path: 
set /p BLUEXOLO_DATA=BlueXolo data path: 

:: To use defined paths comment the two lines above then uncomment and set
:: the values down here
::BLUEXOLO_DIR=/your/bluexolo
::BLUEXOLO_DATA=/your/bluexolo-data

:: Update and run docker image
echo Fetching latest version of BlueXolo . . .
docker pull bluexolo/bluexolo
echo Running BlueXolo . . .
docker run -d --privileged --rm -p 8000:8000 -h bluexolo -e container=docker -v %BLUEXOLO_DIR%:/opt/BlueXolo-src -v %BLUEXOLO_DATA%:/var/lib/postgresql --name bluexolo bluexolo/bluexolo

:: Configure bluexolo user and check required directories
echo Running startup configurations . . .
docker exec -ti bluexolo bash -c "/opt/BlueXolo-src/tools/check_dirs.sh && sleep 15"
docker exec -ti bluexolo bash -c "/opt/BlueXolo-src/docker/scripts/config-user.sh"

echo:
exit 0

::===============================================================
:: End of script
::===============================================================