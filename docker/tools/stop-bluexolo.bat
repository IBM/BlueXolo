@echo off

title Stop BlueXolo
echo:

set OPTION=%1

:: Kill BlueXolo and BlueXoloAssistant running containers
docker kill bluexolo bluexolo_assistant

:: Remove network for offline virtual assistance
docker network rm offline_assistant

:: Remove offline execution resources
if %OPTION%==--offline (
    docker kill language_server
    docker network rm offline_assistant
)

exit 0

::===============================================================
:: End of script
::===============================================================