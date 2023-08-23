# Creating the servable Docker Artifact

## Prequisities

1.  Since this is a Makefile-driven build, just install make for your particular operation system

### Ubuntu on Linux

1. If previous install, Uninstall docker via snap
    ```shell
    snap remove docker
    ```
2. Follow the directions on the site (https://docs.docker.com/desktop/install/ubuntu/)
3. Install make and curl
   ```shell
   sudo apt install -y make curl
   ```

### MacOS (tested on Version 12.1)

Multiple options exists, i.e., https://apple.stackexchange.com/questions/373888/how-do-i-start-the-docker-daemon-on-macos

This is the only one that worked in my case ...

1. brew install --cask docker

2. brew install docker-machine

3. brew install colima  

4. colima start

5. docker ps -a



## How to build docker image

1. Run the command:
   ```shell
   make docker-image
   ```

## How to test the docker image

1. Run the command in one terminal:
   ```shell
   make docker-server
   ```
2. Run the request command in another terminal
   ```shell
   make docker-server-test
   ```
   If it returns the payload as specified in config.json, woot!  Profit!
4. Press ctrl-C in the first terminal to stop the server.
## How to clean up the docker image
1. Run the command:
   ```shell
   make clean
   ```
