# psMonitor
The project for process performance monitor. Currently that's only CPU and Memory monitor for sample.
> In the future it will be modified the name-- **GemeloEyes**

## Prerequisite
In this project that used:
* Docker 20.10.8
* Python 3.7.0+

## Getting Started
### Setup
* `.env` file:
    ```
    DB_HOST=[The host name of DB]
    DB_PORT=[The port of DB]
    DB_USER=[The username of DB] (Optional)
    DB_PASSWORD=[The password of DB] (Optional)
    ```
* install the dependency packages by command:
    * `pip install -r requirements.txt`

* If you want to install docker in raspberry pi, please use the shell script in `docker` directory:
    * `bash docker-install.sh`

### Start
* You want to run program by yourself. Please follow the steps:
    1. Go to the `docker` directory and run this command:
        * `docker-compose up -d`
    2. Go to the `psMonitor` directory and run the python program:
        * `python main.py`

### Stop
1. Go to the `docker` directory and run this command:
    `docker-compose down`
2. You can use `ctrl+c` to terminate the process.

## Code Template for custom
* The code constructs by template pattern:
    ```python
    import sys
    print(sys.path)

    from templates.deviceMonitor.CPUandMemoryForDM import CPUandMemoryForDM
    import os
    import time

    from dotenv import load_dotenv
    from logger.logger import Logger
    logger = Logger.instance()

    if __name__=='__main__':
        """ Entry point """
        load_dotenv()
        logger.info('Load environment variables successfully.')
        cpuAndMemDM = CPUandMemoryForDM()
        while True:
            cpuAndMemDM.monitor()
    ```
* Step of writing code:
    1. Use the monitor template, you can design what the template of monitor you want by yourself
        * `ps = YourselfMonitorTemplate(args...)` is your monitor template. 
        * Just extends the `DeviceMonitor` in `psMonitor/templates/deviceMonitor` directory to implement the template the you want.
    2. Remember to put `monitor` method in loop.
        * `ps.monitorThroughNetwork()` in `while loop` or `for loop`.
        * you can use `time.sleep` to control the monitor frequency.

## Test
* `.env_test` file:
    ```
    DB_HOST=[The host name of DB]
    DB_PORT=[The port of DB]
    DB_USER=[The username of DB]
    DB_PASSWORD=[The password of DB]
    ```

* The following is test cases:
    * Test that get system performance.
    * Test that writes data that monitored into database.
    * Test the whole monitor mechanism (code in template method) on running.  

## Design Blueprint
### System Design
The system design of psMonitor:
![GemeloEyes](./docs/GemeloEyes-System-Design.png)

### Code Design
The code design of psMonitor:
![GemeloEyes](./docs/GemeloEyes-Program-Design.png)


## Contribution
* Hao-Ying Cheng (MaskerTim)
    * Email: t109598001@ntut.org.tw
    * Affliation: National Taipei University of Technology