# Makefile driven build for flask-wrapper docker image
include ../../serve-yourself-env-auth.env

# Explicitly pull serve-yourself environment variables
DOCKER_HUB_USERNAME=${SY_ENV_DOCKERHUB_USERNAME}

DOCKER_ARTIFACT_NAME=flask-wrapper-injection
TARGET_REPO=${DOCKER_HUB_USERNAME}/${DOCKER_ARTIFACT_NAME}

all:
	@echo "Running end-to-end test for local k8s"
	make deploy-all
	### Testing service endpoint
	make test-flask-injection
	### Finished testing service endpoint
	make teardown-all

deploy-all:
	make deploy-local-kind-k8s
	make deploy-flask-injection
	# Wait for the k8s deploy to finish
	python3 ../common/k8s/k8s_wait.py --type=deployment.app --name=flask-injection-wrapper-deployment --abstract-state=deployed


teardown-all:
	make teardown-flask-injection
	# Wait for the k8s teardown to finish
	python3 ../common/k8s/k8s_wait.py --type=deployment.app --name=flask-injection-wrapper-deployment --abstract-state=torndown
	make teardown-local-kind-k8s

deploy-local-kind-k8s:
	kind create cluster --config=expose-ports-kind.yaml

teardown-local-kind-k8s:
	kind delete cluster

deploy-flask-injection:
	kubectl apply -f deployment.yaml

teardown-flask-injection:
	kubectl delete svc flask-injection-service
	kubectl delete deployment.app flask-injection-wrapper-deployment

port-forward-flask-injection:
	kubectl port-forward deployments/flask-injection-wrapper-deployment 8888:8888

test-flask-injection:
	curl localhost:30000