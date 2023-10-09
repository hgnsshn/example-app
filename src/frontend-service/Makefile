REPO ?= local-registry:5200
APP_NAME ?= frontend-service
GIT_HASH ?= $(shell git log --format="%h" -n 1)

build:
	docker build --tag ${REPO}/${APP_NAME}:${GIT_HASH} .
push:
	docker push ${REPO}/${APP_NAME}:${GIT_HASH}
release:
	docker pull ${REPO}/${APP_NAME}:${GIT_HASH}
	docker tag ${REPO}/${APP_NAME}:${GIT_HASH} ${REPO}/${APP_NAME}:latest
	docker push ${REPO}/${APP_NAME}:latest
