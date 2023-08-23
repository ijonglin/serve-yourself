# Makefile driven build for flask-wrapper docker image
include ../../serve-yourself-env-auth.env

# Explicitly pull serve-yourself environment variables
DOCKER_HUB_USERNAME=${SY_ENV_DOCKERHUB_USERNAME}
DOCKER_HUB_AUTH=${SY_ENV_DOCKERHUB_AUTH}

DOCKER_ARTIFACT_NAME=flask-wrapper-injection
TARGET_REPO=${DOCKER_HUB_USERNAME}/${DOCKER_ARTIFACT_NAME}

all:
	@echo "See Makefile for all valid targets."

test:
	@echo "To test this image, run the make docker-server in one window, and"
	@echo "    then run make docker-server-test in another window."

# Starts the docker image with a simple bash in the docker environment
docker-image:
	docker build . -t $(DOCKER_ARTIFACT_NAME)

# Starts the docker image with a simple bash in the docker environment
docker-interactive: docker-image
	docker run --rm -it --entrypoint /bin/bash $(DOCKER_ARTIFACT_NAME)

# Creates extra bash shell on running image
docker-exec: docker-image
	docker exec --it --entrypoint /bin/bash $(DOCKER_ARTIFACT_NAME)

# Runs the service on docker as a flask wrapper on a port determined by the env var FLASKPORT
# DOCKER_SERVER_PORT is then forwarded onto the local machine.
DOCKER_SERVER_PORT=8888
docker-server: docker-image
	docker run --rm -it -e FLASK_PORT=$(DOCKER_SERVER_PORT) -p $(DOCKER_SERVER_PORT):$(DOCKER_SERVER_PORT) $(DOCKER_ARTIFACT_NAME)

docker-server-test:
	curl localhost:8888

dockerhub-login:
	@echo "echo ***HIDDEN*DOCKER*HUB*AUTH*** | docker login -u $(DOCKER_HUB_USERNAME) --password-stdin"
	# Don't output the auth to standard output
	@echo ${DOCKER_HUB_AUTH} | docker login -u $(DOCKER_HUB_USERNAME) --password-stdin

dockerhub-publish:
	docker image tag $(DOCKER_ARTIFACT_NAME) $(TARGET_REPO)
	docker push $(TARGET_REPO)

clean:
	docker rm -f $(DOCKER_ARTIFACT_NAME)
	docker image rm -f $(DOCKER_ARTIFACT_NAME)
	docker system prune

linux-local-secrets-store-init:
	gpg --full-generate-key
	# Get public get identity
	gpg --list-keys
	pass init `gpg -k | head -4 | tail -1 | awk '{print $$1}'`

linux-local-secrets-store-clean:
	@echo "# To clean up the password store use the following commands"
	@echo "    rm -rf ~/.gpupg"
	@echo "    rm -rf ~/.password-store"
	@echo "# However, this kills all password and GPG state.  So beware."

linux-local-secrets-store-clean-force:
	# !!!DANGEROUSLY!!! Cleaning up the password store use the following commands:
	rm -rf ~/.gpupg
	rm -rf ~/.password-store

