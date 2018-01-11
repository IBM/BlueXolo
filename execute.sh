#!/usr/bin/sh
# | - - - - - - - - - - - - - - - - - - - - - - - - - - -  |
# |                    Execution Script                    | 
# |                Last update January 2018                |
# |                  by Francisco Suárez                   |
# | - - - - - - - - - - - - - - - - - - - - - - - - - - -  |
source ./variables.sh
source $VIRTUAL_ENV_PATH/bin/activate
printf "$RED First need set variables.sh with real paths and vars.\n"
printf "\n $BLU ====================================================== \n"

read -p "$BLU Is the first execution? (y/N, default=No)? " answer
case ${answer:0:1} in
    y|Y )
    printf "$GRN \nOk, then let's setup some stuff...\n\n"
    source tools/check_dirs.sh

    printf "$GRN \nPython dependencies\n\n"
    pip install -r requirements.txt

    printf "$GRN \nApply migrations\n\n"
    python manage.py migrate 

    printf "$GRN \nCreate Superuser\n\n"
    python manage.py createsuperuser

    printf "$GRN \nPopulate with some variables\n\n"
    python run_base_migrations.py
    
    printf "$CYN \nDONE, execute again the script.\n\n"
    ;;
    * )
    printf "$GRN \nFirst Seek and destroy ;-).\n\n"
    ps -ef | grep 'celery' | grep -v grep | awk '{print $2}' | xargs kill
    ps -ef | grep 'runserver 0.0.0.0:$PORT' | grep -v grep | awk '{print $2}' | xargs kill    

    printf "$GRN \nRunning Celery.\n\n"
    CELERY_LOG=celery_$(date +'%d_%m_%Y')_log.txt
    nohup celery -A CTAFramework worker -l info  --concurrency=$CONCURRENCY > logs/$CELERY_LOG &
    
    printf "$GRN \nRunning Django.\n\n"
    DJANGO_LOG=django_$(date +'%d_%m_%Y')_log.txt
    nohup python manage.py runserver 0.0.0.0:$PORT > logs/$DJANGO_LOG &
    
    printf "$CYN \nDONE, the project is running on port: $PORT.\n\n "
    printf "Don't forget the directory for Logs:$BASE_DIR/logs \n\n"
    ;;
esac
