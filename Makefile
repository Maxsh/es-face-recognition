SHELL := /bin/bash
APP_NAME ?= ElasticSearch for face recognition
BUILD_KEY ?= es-face-recognition

# build for development (default target)
.PHONY: dev
dev: dev-img | .env
	@echo "$(APP_NAME) is built for development"

.PHONY: dev-img
dev-img: | .env
	# build development docker images - uses --pull to ensure we check the upstream source image for the latest version
	docker-compose build

# create an .env file if one doesn't already exist - this is expected to be run by CI tooling. Engineers should
# manually "cp .env.dist .env" and edit the resulting file before running this makefile.
.env:
	cp .env.dist .env

	# ensure that the .env finishes with a new line so we can safely append to it
	echo "" >> .env

# run the application in a development context
.PHONY: up
up: dev
	docker-compose up -d

# stop the running application
.PHONY: down
down:
	docker-compose down

# stops all containers and removes all files created by this makefile
.PHONY: clean
clean:
	rm -rf build
	@ [[ -f .env ]] && docker-compose down || true

.PHONY: get_vector
get_vector:
	docker-compose run --rm app python src/getVectorFromPicture.py $(ARGS)

.PHONY: recognize
recognize:
	docker-compose run --rm app python src/recognizeFaces.py $(ARGS)