@echo off

title Stop BlueXolo
echo:

:: Kill BlueXolo and BlueXoloAssistant running containers
docker kill bluexolo bluexolo_assistant

:: Remove network for offline virtual assistance
docker network rm offline_assistant

exit 0

::===============================================================
:: End of script
::===============================================================