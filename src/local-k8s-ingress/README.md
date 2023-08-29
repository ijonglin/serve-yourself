# Local kubernetes testing

In this section, we will be deploying a local instance of the flask wrapper Docker image.

From the serve-yourself infrastructure requirements, local k8s testbed will be __MISSING__ the 
following requirements:

* IDENTITY:  Simple basic auth secret sharing.
* NETWORK: Since we're local, the output is placed on a reserved port on localhost
* COST:  Because it's your own machine, there's no cost to you except for the electricity.

TODO: Add basic generated token as a requirement for calling the endpoint.

## Prerequisites

1. Install kind from https://kind.sigs.k8s.io/docs/user/quick-start/#installation
2. Modify the Docker image specified in line 20 of [deployment.yaml](deployment.yaml) to the location
   of the Docker registry where you have stored the [example serve-yourself docker image](../docker-artifact)

## Automatic Testing

1. Run the following command:
   ```
   make
   ```
   This command will bring up the local k8s cluster, deploy a simple load balanced instance of the
   Docker image specified in line 20 of [deployment.yaml](deployment.yaml), test the endpoint, and
   then, if successful, tear down cluster.

## Manual Testing on a local cluster created by kind (for reference)

1. Install package to create a local k8s cluster for testing
    Follow directions on https://kind.sigs.k8s.io/docs/user/quick-start/#installing-from-release-binaries
2. Create local cluster with kind:
    ```shell
    /usr/local/bin/kind create cluster
    ```
3. Create local pod:
    ```shell
    kubectl run simple-cms   --labels="name=simple-cms"   --image=jetstack/simple-cms:1.0.0
    kubectl run simple-hello-world   --labels="name=simple-hello-world"   --image=nginxdemos/hello:latest
    ```
4. Confirm pod exists:
    ```shell
    kubectl get pod
    ```
5. Create front-end service router:
    ```shell
    k apply -f service.yaml 
    k apply -f service-hello-world.yaml 
    ```
6. Access endpoint from port forward
    ```shell
    kubectl port-forward services/simple-cms 8081:80
    ```
    OR
    ```shell
    kubectl port-forward services/simple-hello-world 8081:80
    ```
7. Test output in different terminal:
    ```shell
    curl http://localhost:8081
    ```

## Notes 

Many scripts are modified from: https://kind.sigs.k8s.io/docs/user/ingress/
Requires install 
sudo apt install apache2-utils
sudo apt install uuid