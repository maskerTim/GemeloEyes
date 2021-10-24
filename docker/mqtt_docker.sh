# declare to use /bin/bash
#!/bin/bash

# running mqtt by docker
# create docker network
if [ ! "$(docker network ls | grep mqttNetwork)" ]; then
    echo "Creating mqttNetwork network ..."
    docker network create --gateway 172.14.0.1 --subnet 172.14.0.0/24 -d bridge mqttNetwork
else
  echo "mqttNetwork network existed."
fi

# running mosquitto container
docker run -it --name mqttbroker --network mqttNetwork --ip 172.14.0.10 -p 1883:1883 -p 9001:9001 -v \
"$(pwd)/mqtt_conf/mosquitto.conf:/mosquitto/config/mosquitto.conf" -v "$(pwd)/mqtt_conf/mosquitto_data:/mosquitto/data" \
-v "$(pwd)/mqtt_conf/mosquitto_log:/mosquitto/log" -d --rm eclipse-mosquitto
