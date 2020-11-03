#!/bin/bash -

# | - - - - - - - - - - - - - - - - - - - - - - - - - - -  |
# |      Script for Robot Framework installation           |
# |           and bluexolo user configurations             |
# |              Last update November 2020                 |
# |                  by Santiago Valle                     |
# | - - - - - - - - - - - - - - - - - - - - - - - - - - -  |

# Install robot framework
pip3 install robotframework robotframework-requests robotframework-selenium2library robotframework-sshlibrary

# Set a password for the bluexolo user
echo 'bluexolo:bluexolo' | chpasswd

# Change directory permissions for bluexolo user
chmod -R 775 /home/bluexolo

exit 0