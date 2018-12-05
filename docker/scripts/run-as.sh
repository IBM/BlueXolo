#!/bin/bash -
##################################################
## (C) COPYRIGHT IBM Corp. 2018
##################################################
#  Description:  Run as specific user
#
#       Author:  Fernando Quintero (fqa), quintero@mx1.ibm.com
#      VERSION:  1.0
#      Created:  08/25/18 21:08
#     Revision:  ---
##################################################
#

# Name of script.
SCRIPT=`basename ${BASH_SOURCE[0]}`
OPT_USER=NONE
OPT_COMMAND=NONE

#Set fonts for Help.
NORM=`tput sgr0`
BOLD=`tput bold`
REV=`tput smso`

#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  function_warning()
#   DESCRIPTION:
#-------------------------------------------------------------------------------
function warning() {
  echo -e "$*"
}


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  ABOUT()
#   DESCRIPTION:  Provide help about script
#-------------------------------------------------------------------------------
function ABOUT {
  echo -e  \\n"About ${SCRIPT} tool"\\n
  echo -e "Basic usage: $SCRIPT -u <user> -c <command>"\\n
  echo "The following switches are recognized."
  echo "-u  --Specify the user. this is required."
  echo "-c  --Specify the command. this is required."
  echo -e  "Example: $SCRIPT -u [user] -c [command] "\\n
  exit 1
}


NUMARGS=$#
if [ $NUMARGS -eq 0 ]; then
  echo "You haven't passed any parameters, exiting..."
  exit 1
fi

while getopts :u:c: FLAG; do
  case $FLAG in
    c)
      export OPT_COMMAND=$OPTARG
    ;;
    u)
      export OPT_USER=$OPTARG
    ;;
    \?) #unrecognized option - show help
      echo -e \\n"Option -$OPTARG unrecognized."
      echo -e "Use $SCRIPT -h to see the help documentation."\\n
      exit 2
    ;;
  esac
done

# Check if the -u option has been given.
# -------------------------------------
if [ "$OPT_USER" == "NONE" ]; then
  warning \\n"Option -u is required."
  ABOUT
fi
# Check if the -c option has been given.
# -------------------------------------
if [ "$OPT_COMMAND" == "NONE" ]; then
  warning \\n"Option -c is required."
  ABOUT
fi


nohup su -l $OPT_USER -c $OPT_COMMAND &
