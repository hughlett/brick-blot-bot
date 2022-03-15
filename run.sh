COMPOSE_PATH=/volume1/GithubProjects/brick-blot-bot/docker-compose.yml
PROJECT_PATH=/volume1/GithubProjects/brick-blot-bot

cd ${PROJECT_PATH} && git pull
docker-compose -f ${COMPOSE_PATH} up --build --abort-on-container-exit && docker-compose -f ${COMPOSE_PATH} down
