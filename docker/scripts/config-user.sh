#!/bin/bash -

# | - - - - - - - - - - - - - - - - - - - - - - - - - - -  |
# |        Script for bluexolo user configurations         |
# |              Last update November 2020                 |
# |                  by Santiago Valle                     |
# | - - - - - - - - - - - - - - - - - - - - - - - - - - -  |

# Set a password for the bluexolo user
echo 'bluexolo:bluexolo' | chpasswd

# Change directory permissions for bluexolo user
chmod -R 775 /home/bluexolo

exit 0