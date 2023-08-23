# serve-yourself-private

## Goal 

The goal of this project is to serve a Docker image and its endpoints on internet-accessible, 
but limited access endpoint in a scalable cloud infrastructure with well-defined lifecycle events 
(i.e. creation and teardown). In short, it is Object Oriented Principles (OOP) 
applied to a cloud service infrastructure, where:

* Functionality is defined by the specified docker image
* Data/Control Access is defined by SSO identity of the callee 
* Lifecycle Control is defined by cloud authentication
* Internal state and provisioned infrastructure is completely managed by the object
* Secret Managements that is compatible with the requirements above

## Specifications

The end-to-end system requirements are, as follows:

1. Requires a limited set of cloud authentication tokens to transition lifecycle on the 
     provisioned cloud infrastructure.
2. Runs any arbitrary docker image that exposes its functionality on a specified network port
3. Limits Access to Exposed Dataplane Endpoints to a set of Single Sign On (SSO) users via JWT tokens
4. Limits Access to Exposed Control Endpoints to a set of Single Sign On (SSO) users via JWT tokens
5. Exposes the cost of the provisioned infrastructure in actual currency
6. Maintains basic performance metrics on provisioned infrastructure
7. Multiple instances of this service and provisioned infrastructure can coexist for the same set of cloud authentication tokens

## Prerequisites

* Python 3.8+
* kubectl  (https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)

## Implementations

* [docker-artifact](src/docker-artifact) -- a Flask-based network wrapper for Python code, retargetable to wrap
    any arbitrary Python calls on an image
* [Local k8s](src/local-k8s) -- k8s cluster on your local machine started by kind
