#!/bin/bash
set -e

CONTAINER_NAME=local-jenkins

cleanup_and_exit() {
    echo -e "\nCleaning up and exiting please wait..."
    docker stop $CONTAINER_NAME > /dev/null 2>&1
    docker rm $CONTAINER_NAME > /dev/null 2>&1
    exit 0
}

# Trap interrupt signal (Ctrl+C) and call cleanup_and_exit function
trap 'cleanup_and_exit' INT

export LOCAL_JENKINS_DOCKER_SOCKET="/run/user/1000/docker.sock"
export LOCAL_JENKINS_DOCKER_BIN="/home/nick/bin/docker"

# Set the paths and variables
PORT_MAPPING="8080:8080"

# docker-compose up --build 
docker build -t ${CONTAINER_NAME} .

# docker container rm local-jenkins

# Run the Docker container
docker run -d \
  --name ${CONTAINER_NAME} \
  -p ${PORT_MAPPING} \
  -v $(pwd)/../.:/mnt/cicd-django-demo:ro \
  -v ${LOCAL_JENKINS_DOCKER_SOCKET}:/var/run/docker.sock \
  -v ${LOCAL_JENKINS_DOCKER_BIN}:/usr/bin/docker \
  ${CONTAINER_NAME}

docker logs -f ${CONTAINER_NAME}


