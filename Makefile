# Global Deployments settings required for all component builds
# !!!! ALL AUTHENTICATION GOES INTO a local file sys-env-auth.env !!!!!

# Docker Hub Repo Information
# Remember: Never check into
include serve-yourself-env-auth.env

dockerhub-all:
	cd src/docker-artifact; make docker-image docker-login dockerhub-publish
