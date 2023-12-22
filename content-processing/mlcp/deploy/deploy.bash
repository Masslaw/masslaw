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

IMAGE_NAME=mlcp-text-extraction-$STAGE
DOCKERFILE=text-extraction.dockerfile
docker build -t $IMAGE_NAME -f deploy/$DOCKERFILE .
docker tag $IMAGE_NAME:latest 746826375642.dkr.ecr.us-east-1.amazonaws.com/$IMAGE_NAME:latest
docker push 746826375642.dkr.ecr.us-east-1.amazonaws.com/$IMAGE_NAME:latest

IMAGE_NAME=mlcp-knowledge-extraction-eng-$STAGE
DOCKERFILE=knowledge-extraction-eng.dockerfile
docker build -t $IMAGE_NAME -f deploy/$DOCKERFILE .
docker tag $IMAGE_NAME:latest 746826375642.dkr.ecr.us-east-1.amazonaws.com/$IMAGE_NAME:latest
docker push 746826375642.dkr.ecr.us-east-1.amazonaws.com/$IMAGE_NAME:latest

echo "Shutting down Docker..."
osascript -e 'quit app "Docker"'
echo "Docker has been shut down."
