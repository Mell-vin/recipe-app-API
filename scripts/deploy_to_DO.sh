#!/bin/sh

# Define Docker image details
IMAGE_NAME="gumaiitsupport/gumai_db:v2.0.0"
CONTAINER_NAME="gumai_db"

# Pull the latest version of the image
docker pull $IMAGE_NAME

# Check if the container is running, and if so, stop and remove it
if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Run a new container from the pulled image
docker-compose pull
run: docker-compose -f docker-compose.prod.yml run -e DB_HOST=${{ secrets.DB_HOST }} -e POSTGRES_DB=${{ secrets.DB_NAME }} -e POSTGRES_USER=${{ secrets.DB_USER }} -e POSTGRES_PASSWORD=${{ secrets.DB_PASS }} up

# Optionally, if you use Docker Compose and have a docker-compose.yml file, you can:

# Any additional steps, like clearing caches, restarting related services, etc., can be added here.

