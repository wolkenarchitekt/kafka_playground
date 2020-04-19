DOCKER_NAME = monitoring_service

build:
	docker build -t $(DOCKER_NAME) .

run:
	docker run -it --rm $(DOCKER_NAME)

shell:
	docker run -it --rm $(DOCKER_NAME) bash

ipython:
	docker run -it --rm $(DOCKER_NAME) ipython
