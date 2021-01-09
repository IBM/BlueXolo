@echo off

title Stop BlueXolo
echo:

:: Kill BlueXolo and BlueXoloAssistant running containers
docker kill bluexolo bluexolo-assistant

exit 0

::===============================================================
:: End of script
::===============================================================