#!/bin/bash


# Run bluexolo 
nohup docker run --privileged \
 -p 8000:8000 \
 -h bluexolo \
-e container=docker \
-v /sys/fs/cgroup:/sys/fs/cgroup \
-v /home/raaul19/BlueXolo:/opt/BlueXolo-src \
-v /opt/bluexolo-data:/var/lib/postgresql \
--name bluexolo \
bluexolo/bluexolo  &
