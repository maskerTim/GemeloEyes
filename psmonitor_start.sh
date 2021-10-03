#!/bin/bash

# run the docker services
cd "./docker"
docker-compose up -d

# run program
python main.py