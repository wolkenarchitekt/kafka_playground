DOCKER_NAME = website
NGINX_PORT = 80

build:
	docker build -t $(DOCKER_NAME) .

run:
	docker run -it --rm -p $(NGINX_PORT):80 $(DOCKER_NAME)

shell:
	docker run -it --rm $(DOCKER_NAME) bash

ipython:
	docker run -it --rm $(DOCKER_NAME) ipython
