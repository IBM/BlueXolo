#!/usr/bin/bash

#script
echo 'Welcome back Mr. Anderson'
echo "Let's create some dirs First"
mkdir -p media/test_keywords
echo " . "
mkdir -p media/zips
echo " . . "
mkdir -p media/test_result
echo " . . . "
echo "ok, the dirs have created."
echo "Now need run Celery on background"
ps -ef | grep 'celery' | grep -v grep | awk '{print $2}' | xargs kill
nohup celery -A CTAFramework worker -l info &
echo "Then run python, that's your Task my friend. See u :3"
