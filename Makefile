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

config:
	$(DOCKER_COMPOSE_CMD) config

logs:
	$(DOCKER_COMPOSE_CMD) logs -f

lint: config http-check-producer-lint http-check-consumer-lint

test-unit: http-check-producer-test http-check-consumer-test

test-smoke:
	# Smoke test producing and consuming a single http check
	$(MAKE) http-check-producer-run-once
	$(MAKE) http-check-consumer-run-once

test-integration: integration-tests-run

test: test-unit test-smoke integration-tests-run

http-check-producer-ipython:
	$(DOCKER_COMPOSE_CMD) run --rm http_check_producer ipython

http-check-producer-build:
	$(DOCKER_COMPOSE_CMD) build http_check_producer

http-check-producer-bash:
	$(DOCKER_COMPOSE_CMD) run --rm http_check_producer bash

http-check-producer-run:
	$(DOCKER_COMPOSE_CMD) run --rm http_check_producer

http-check-producer-run-once:
	$(DOCKER_COMPOSE_CMD) run --rm http_check_producer \
		/wait-for-it.sh -t 60 kafka:8081 -- \
		http_check_producer -d run-once --url http://website

http-check-producer-test:
	$(DOCKER_COMPOSE_CMD) run --no-deps --rm http_check_producer pytest

http-check-producer-lint:
	$(DOCKER_COMPOSE_CMD) run --no-deps --rm http_check_producer flake8
	$(DOCKER_COMPOSE_CMD) run --no-deps --rm http_check_producer mypy http_check_producer


http-check-consumer-ipython:
	$(DOCKER_COMPOSE_CMD) run --rm http_check_consumer ipython

http-check-consumer-build:
	$(DOCKER_COMPOSE_CMD) build http_check_consumer

http-check-consumer-bash:
	$(DOCKER_COMPOSE_CMD) run --rm http_check_consumer bash

http-check-consumer-run:
	$(DOCKER_COMPOSE_CMD) run --rm http_check_consumer

http-check-consumer-run-once:
	$(DOCKER_COMPOSE_CMD) run --rm http_check_consumer http_check_consumer -d run-once

http-check-consumer-test:
	$(DOCKER_COMPOSE_CMD) run --no-deps --rm http_check_consumer pytest

http-check-consumer-lint:
	$(DOCKER_COMPOSE_CMD) run --no-deps --rm http_check_consumer flake8
	$(DOCKER_COMPOSE_CMD) run --no-deps --rm http_check_consumer mypy http_check_consumer


postgres-logs:
	$(DOCKER_COMPOSE_CMD) logs -f postgres


integration-tests-build:
	$(DOCKER_COMPOSE_CMD) build integration-tests

integration-tests-run:
	$(DOCKER_COMPOSE_CMD) run integration-tests
