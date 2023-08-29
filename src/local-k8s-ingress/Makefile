# Makefile driven build for flask-wrapper docker image
include ../../serve-yourself-env-auth.env

# Explicitly pull serve-yourself environment variables
DOCKER_HUB_USERNAME=${SY_ENV_DOCKERHUB_USERNAME}

DOCKER_ARTIFACT_NAME=flask-wrapper-injection
TARGET_REPO=${DOCKER_HUB_USERNAME}/${DOCKER_ARTIFACT_NAME}

all:
	@echo "Running end-to-end test for local k8s"
	@echo "**********************"
	@echo "** Deploy Section"
	@echo "**********************"
	make deploy-all
	### Make sure all components are ready
	python3 ../common/k8s/k8s_wait.py --type=pod --name=foo-app --abstract-state=deployed
	python3 ../common/k8s/k8s_wait.py --type=pod --name=bar-app --abstract-state=deployed
	python3 ../common/k8s/k8s_wait.py --namespace=ingress-nginx --type=deployment.apps --name=ingress-nginx-controller --abstract-state=deployed
	python3 ../common/k8s/k8s_wait.py --type=pod --name=bar-app --abstract-state=deployed
	python3 ../common/k8s/k8s_wait.py --type=ingress --name=example-ingress --abstract-state=deployed
	python3 ../common/k8s/k8s_wait.py --type=deployment.app --name=flask-injection-wrapper-deployment --abstract-state=deployed
	# TODO: Consider whether the above tests _should_ be sufficient to guarantee endpoint correctness.
	#       add another test (or part of start-up deployment) to ensure that it's ready by this point
	@echo "**********************"
	@echo "** Test Section"
	@echo "**********************"
	echo "*** NOTE: Initial call may not be ready due to cold start issues."
	make test-flask-injection
	make test-flask-injection-secure
	sleep 5
	echo "*** NOTE: But five seconds later, it's all good."
	make test-flask-injection
	make test-flask-injection-secure
	### Finished testing service endpoint
	@echo "**********************"
	@echo "** Teardown Section"
	@echo "**********************"
	make teardown-all

##########################
# Deployments
##########################

deploy-local-kind-k8s:
	kind create cluster --config=expose-ports-kind-ingress.yaml

deploy-http-secret:
	rm -f auth generated_password_uuid.txt
	# Generate secret as uuid and make sure it read-only local user-only for security practices
	(umask 377; uuid -o generated_password_uuid.txt)
	# Note: Told that it must be named auth for some reason.
	cat generated_password_uuid.txt | htpasswd -ci auth USERNAME
	# To verify
	cat generated_password_uuid.txt | htpasswd -vi auth USERNAME
	kubectl create secret generic basic-auth --from-file=auth
	@echo "*** Generated password is stored in local read-only file genereated_password_uuid.txt under user USERNAME"

deploy-ingress-controller:
	kubectl apply -f deploy_ingress_controller.yaml

deploy-service:
	kubectl apply -f deploy_service.yaml

deploy-flask-injection:
	kubectl apply -f deployment.yaml

deploy-all:
	make deploy-local-kind-k8s
	make deploy-http-secret
	make deploy-ingress-controller
	sleep 15  # Wait until ingress controller resources show up, TODO: Replace with something more deterministic
	kubectl wait --namespace ingress-nginx \
  		--for=condition=ready pod \
  		--selector=app.kubernetes.io/component=controller \
  		--timeout=90s
	make deploy-service

##########################
# Teardown
##########################

teardown-all:
	make teardown-foobar
	make teardown-flask-injection
	# Wait for the k8s teardown to finish
	python3 ../common/k8s/k8s_wait.py --type=pod --name=foo-app --abstract-state=torndown
	python3 ../common/k8s/k8s_wait.py --type=pod --name=bar-app --abstract-state=torndown
	python3 ../common/k8s/k8s_wait.py --type=deployment.app --name=flask-injection-wrapper-deployment --abstract-state=torndown
	make teardown-http-secret
	make teardown-local-kind-k8s

teardown-http-secret:
	kubectl delete secret basic-auth
	rm -f auth generated_password_uuid.txt

teardown-local-kind-k8s:
	kind delete cluster

teardown-flask-injection:
	kubectl delete svc flask-injection-service
	kubectl delete deployment.app flask-injection-wrapper-deployment

teardown-foobar:
	kubectl delete svc foo-service
	kubectl delete svc bar-service
	kubectl delete pod bar-app
	kubectl delete pod foo-app

port-forward-flask-injection:
	kubectl port-forward deployments/flask-injection-wrapper-deployment 8888:8888


##########################
# Test
##########################

test-flask-injection:
	echo "NOTE: These calls should give a 401 _ERROR_ because they don't have the proper authentication."
	(curl localhost/foo/hostname ; echo "")
	(curl localhost/bar/hostname ; echo "")
	(curl localhost/flask)

test-flask-injection-secure:
	(PASSWORD=`cat generated_password_uuid.txt` ; curl localhost/foo/hostname -u "USERNAME:$${PASSWORD}"; echo "")
	(PASSWORD=`cat generated_password_uuid.txt` ; curl localhost/bar/hostname -u "USERNAME:$${PASSWORD}"; echo "")
	(PASSWORD=`cat generated_password_uuid.txt` ; curl localhost/flask -u "USERNAME:$${PASSWORD}")


##########################
# Sugar/Shortcuts
##########################

clean:
	@echo "Default teardown of kind cluster"
	make teardown-local-kind-k8s

install-deps:
	sudo apt install -y uuid apache2-utils