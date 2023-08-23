FROM ubuntu:22.04

# Add system dependencies
RUN apt update
RUN apt install -y apt-utils dialog
RUN apt install -y python3 python3-venv python3-pip
RUN apt install -y curl

# Add userspace runner
RUN addgroup --gid 1000 flaskrunner
RUN adduser --uid 1000 --gid 1000 --disabled-password --disabled-login flaskrunner
# Switch to userspace runner
USER flaskrunner
WORKDIR /home/flashrunner
# Copy all files specified in the .dockerignore
COPY . .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3","wrapper.py"]