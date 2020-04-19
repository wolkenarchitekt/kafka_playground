DOCKER_COMPOSE_CMD = docker-compose -f docker-compose.yml -f docker-compose.dev.yml

build:
	$(DOCKER_COMPOSE_CMD) build

up:
	$(DOCKER_COMPOSE_CMD) up --force-recreate

restart:
	$(DOCKER_COMPOSE_CMD) restart

clean:
	$(DOCKER_COMPOSE_CMD) down
	$(DOCKER_COMPOSE_CMD) rm -f

logs:
	$(DOCKER_COMPOSE_CMD) logs -f


website-monitor-ipython:
	$(DOCKER_COMPOSE_CMD) run --rm website_monitor ipython

website-monitor-build:
	$(DOCKER_COMPOSE_CMD) build website_monitor

website-monitor-bash:
	$(DOCKER_COMPOSE_CMD) run --rm website_monitor bash

website-monitor-run:
	#$(DOCKER_COMPOSE_CMD) run --rm website_monitor
	#$(DOCKER_COMPOSE_CMD) run --rm website_monitor website_monitor -d run --url http://website --match-regex "Hello"
	$(DOCKER_COMPOSE_CMD) run --rm website_monitor website_monitor -d run --url http://website

website-monitor-test:
	$(DOCKER_COMPOSE_CMD) run --rm website_monitor pytest


website-monitor-db-ipython:
	$(DOCKER_COMPOSE_CMD) run --rm website_monitor_db ipython

website-monitor-db-build:
	$(DOCKER_COMPOSE_CMD) build website_monitor_db

website-monitor-db-bash:
	$(DOCKER_COMPOSE_CMD) run --rm website_monitor_db bash

website-monitor-db-run:
	#$(DOCKER_COMPOSE_CMD) run --rm website_monitor_db
	$(DOCKER_COMPOSE_CMD) run --rm website_monitor_db website_monitor_db -d run

website-monitor-db-test:
	$(DOCKER_COMPOSE_CMD) run --rm website_monitor_db pytest
