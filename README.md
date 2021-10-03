# psMonitor
The project for process performance monitor. Currently that's only CPU and Memory monitor for sample.

## Prerequisite
In this project that used:
* Docker 20.10.8
* Python 3.7.0+

## Setup
* `.env` file:
    ```
    SINGLE_PROCESS_ID=[PID of single process]
    MULTIPLE_PROCESS_ID=[PID of multiple processes, please use comma to split the processes, e.g., 1440,2201]
    SINGLE_PROCESS_NAME=[Name of single process belonging to PID you config]
    MULTIPLE_PROCESS_NAME=[Name of multiple processes belonging to PID you config, please config by ascending order]
    DB_SOFTWARE=[Which DB to select] # still not use
    DB_HOST=[The host name of DB]
    DB_PORT=[The port of DB]
    DB_USER=[The username of DB] (Optional)
    DB_PASSWORD=[The password of DB] (Optional)
    MQTT_HOST=[The host name of MQTT broker]
    MQTT_PORT=[The port of MQTT broker]
    MQTT_USER=[The username of MQTT broker] (Optional)
    MQTT_PASSWORD=[The password of MQTT broker] (Optional)
    ```
* install the dependency packages by command:
    * `pip install -r requirements.txt`

* If you want to install docker in raspberry pi, please use the shell script in `docker` directory:
    * `bash docker-install.sh`

## Build
* run the `psmonitor_setup.sh` to build the project:
    * `bash psmonitor_setup.sh`

## Start
* run the `psmonitor_start.sh` to start the program:
    * `bash psmonitor_start.sh`

* You want to run program by yourself. Please follow the steps:
    1. Go to the `docker` directory and run this command:
        * `docker-compose up -d`
    2. Go to the `psMonitor` directory and run the python program:
        * `python main.py`

## Stop
1. Go to the `docker` directory and run this command:
    `docker-compose down`
2. You can use `ctrl+C` to terminate the process.

## Code Template for custom
* The code constructs by template pattern:
    ```python
    import sys
    print(sys.path)

    from templates.CPUMemWithInfluxDB import CPUMemWithInfluxDB
    from templates.CPUMemWithMQTT import CPUMemWithMQTT
    import os
    import time

    from dotenv import load_dotenv
    from logger.logger import Logger
    logger = Logger.instance()

    if __name__=='__main__':
        """ Entry point """
        load_dotenv()
        logger.info('Load environment variables successfully.')
        # If you want to monitor multiple processes you need to split process' id by comma
        multiple_process_pid = [int(x) for x in os.getenv('MULTIPLE_PROCESS_ID').split(',')]
        """ InfluxDB version """
        # Use the template for monitor. This template is writing to InfluxDB
        ps = CPUMemWithInfluxDB(multiple_process_pid, 0.5)
        # Monitor for loop
        while True:
            # Template method
            ps.monitorWithDB()
            # use sleep method to make the monitor frequency down
            time.sleep(2)
        """ MQTT version """
        # Use the template for monitor. This template is sending to MQTT Broker
        ps = CPUMemWithMQTT(multiple_process_pid, 0.5)
        # Monitor for loop
        while True:
            # Template method
            ps.monitorThroughNetwork()
            # use sleep method to make the monitor frequency down
            time.sleep(2)
    ```
* Step of writing code:
    1. Set what process id you would like to monitor.
        * `multiple_process_pid = [int(x) for x in os.getenv('MULTIPLE_PROCESS_ID').split(',')]`.
        * You can use `top` command in linux to check the pid.
    2. Use the monitor template, you can design what the template of monitor you want by yourself
        * `ps = YourselfMonitorTemplate(multiple_process_pid, 0.5)` is your monitor template. 
        * Just extends the `psMonitorTemplate` in `psMonitor/template` directory to implement the template the you want.
    3. Remember to put `monitor` method in loop.
        * `ps.monitorThroughNetwork()` in `while loop` or `for loop`.
        * you can use `time.sleep` to control the monitor frequency.

## Test
* `.env_test` file:
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
* In test cases, you can use the `top` service for test process or some process you run for test. Then config in your `.env_test`.

* The following is test cases:
    * Test that monitor single process.
    * Test when you take a no existed process.
    * Test that monitors multiple processes.
    * Test that writes data that monitored into database.
    * Test that sends data that monitored through network.
    * Test the whole monitor mechanism (code in template method) on running.  

## Contribution
* Hao-Ying Cheng (MaskerTim)
    * Email: t109598001@ntut.org.tw
    * Affliation: National Taipei University of Technology