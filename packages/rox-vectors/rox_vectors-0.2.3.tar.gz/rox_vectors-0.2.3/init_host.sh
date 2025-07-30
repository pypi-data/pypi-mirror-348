#!/bin/bash

export USER_UID=$(id -u)
export USER_GID=$(id -g)

mkdir -p /var/tmp/container-extensions

source config.sh

# build docker image
docker build -t $DEV_IMG --build-arg USER_UID=$USER_UID --build-arg USER_GID=$USER_GID -f .devcontainer/Dockerfile .
