#!/bin/bash

# | - - - - - - - - - - - - - - - - - - - - - - - - - - -  |
# |    Script for create the directory schema on media     |
# |                Last update January 2018                |
# |                  by Francisco Suárez                   |
# | - - - - - - - - - - - - - - - - - - - - - - - - - - -  |
DIRS_SCHEMA=(
    "test_keywords"
    "zip"
    "test_result"
    "test_cases"
    "test_suites"
    "keywords"
    "profiles"
    )
echo "Checking the media schema"
MEDIA_DIR="/opt/BlueXolo-src"
for i in "${DIRS_SCHEMA[@]}"
do
    if [ ! -d "$MEDIA_DIR/media/$i" ]; then
    mkdir "$MEDIA_DIR/media/$i"
    printf "$CYN Created\n\n"
fi
done
