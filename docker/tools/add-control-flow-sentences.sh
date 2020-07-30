#!/bin/bash
docker exec -it bluexolo sh -c "cd /opt/BlueXolo/ && python3 manage.py initialize_robot && exit"