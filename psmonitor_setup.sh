#!/bin/bash

# install dependency library
pip install -r requirements.txt

# docker compose build image
cd "./docker"
docker-compose build