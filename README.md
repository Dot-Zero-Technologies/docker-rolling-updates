# Docker Rolling Updates
## Requirements
This only works with Docker Compose as it uses `docker compose up -d --no-recreate` to start containers after updating.

## Features
Docker Rolling Updates automatically updates all running Docker containers whenever a new version is available on [Docker Hub](https://hub.docker.com/).

## Getting started
1. Copy or rename the `.env.example` to `.env` and enter Docker Hub credentials as well as any other configuration.
2. Run `pip3 install -r requirements.txt` to install the required packages.
3. Try running `sudo python3 ./app.py` to test the configuration. Stop the application with `Ctrl + C`.
4. Run `sudo python3 ./setup.py` to install Docker Rolling Updates and to start on system start.
5. To start the service run `sudo systemctl start docker-rolling-updates.service`.