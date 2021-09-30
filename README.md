# psMonitor
The project for process performance monitor

## Setup
* `.env` file
```
SINGLE_PROCESS_ID=[PID of single process]
MULTIPLE_PROCESS_ID=[PID of multiple processes, please use comma to split the processes, e.g., 1440,2201]
NOEXIST_PROCESS_ID=[PID of not existed process]
SINGLE_PROCESS_NAME=[Name of single process belonging to PID you config]
MULTIPLE_PROCESS_NAME=[Name of multiple processes belonging to PID you config, please config by ascending order]
DB_SOFTWARE=[Which DB to select] # still not use
DB_HOST=[The host name of DB]
DB_PORT=[The port of DB]
DB_USER=[The username of DB]
DB_PASSWORD=[The password of DB]
MQTT_HOST=[The host name of MQTT broker]
MQTT_PORT=[The port of MQTT broker]
MQTT_USER=[The username of MQTT broker]
MQTT_PASSWORD=[The password of MQTT broker]
```
* install the dependency packages by command:
`pip install -r requirements`

* If you want to install docker in raspberry pi, please use the shell script in `docker` directory:
`bash docker-install.sh`