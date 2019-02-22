#!/bin/bash

# Run bluexolo 

docker run --privileged \
-ti -p 8000:8000 \
-e container=docker \
-v /sys/fs/cgroup:/sys/fs/cgroup \
bluexolo
