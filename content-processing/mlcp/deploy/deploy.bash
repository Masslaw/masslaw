#!/bin/bash

echo "Deployment stage (e.g. - dev, prod):"
read STAGE

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 746826375642.dkr.ecr.us-east-1.amazonaws.com

docker info > /dev/null 2>&1
STATUS=$?

if [ $STATUS -eq 0 ]; then
    echo "Docker is running. Proceeding..."
else
    echo "Docker is not running. Attempting to start Docker..."
    open --background -a Docker

    echo "Waiting for Docker to start..."

    checks=0
    max_checks=20
    while [ $checks -lt $max_checks ]; do
      sleep 3

      docker info > /dev/null 2>&1
      STATUS=$?
      if [ $STATUS -eq 0 ]; then
        echo "Docker Daemon is now running."
        break
      fi
      checks=$((checks + 1))
    done

    if [ $checks -eq $max_checks ]; then
      echo "Docker didn't start within the expected time. Exiting..."
      exit 1
    fi
fi

cd ..
docker build -t mlcp-$STAGE -f deploy/Dockerfile .
docker tag mlcp-$STAGE:latest 746826375642.dkr.ecr.us-east-1.amazonaws.com/mlcp-$STAGE:latest
docker push 746826375642.dkr.ecr.us-east-1.amazonaws.com/mlcp-$STAGE:latest
