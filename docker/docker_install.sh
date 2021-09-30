# Install for raspberry pi
# declare to use /bin/bash
#!/bin/bash

sudo apt update

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

# add a non-root user to docker group
_user="$(id -u -n)"
sudo usermod -aG docker $_user