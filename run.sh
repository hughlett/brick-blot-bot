#!/bin/bash

PROJECT_PATH=`dirname $0`
COMPOSE_PATH=${PROJECT_PATH}/docker-compose.yml

cd ${PROJECT_PATH} && git pull
docker-compose -f ${COMPOSE_PATH} up --build --abort-on-container-exit && docker-compose -f ${COMPOSE_PATH} down
