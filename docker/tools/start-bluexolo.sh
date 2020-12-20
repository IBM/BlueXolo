#!/bin/bash


# Run bluexolo 
nohup docker run --privileged \
 -p 8000:8000 \
 -h bluexolo \
-e container=docker \
-v /sys/fs/cgroup:/sys/fs/cgroup \
-v /opt/sources/BlueXolo:/opt/BlueXolo-src \
-v /opt/bluexolo-data:/var/lib/postgresql \
--name bluexolo \
bluexolo/bluexolo  &

# Configure bluexolo user
docker exec -ti bluexolo bash -c "/opt/BlueXolo-src/docker/scripts/config-user.sh && /opt/BlueXolo-src/tools/check_dirs.sh"

exit 0

