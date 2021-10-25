import sqlite3
from .DBSample import DBSample
from logger.logger import Logger
logger = Logger.instance()

class DBSqlite3(DBSample):
    """ Database Sqlite3 handler """

    def __init__(self, host) -> None:
        super().__init__(host)

    def _connectTo(self):
        try:
            self._dbHandler = sqlite3.connect(self._host)
            logger.info('sqlite connection succeeds')
            # check the table exists or not, if not, create a table
            cursor = self._dbHandler.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='device_performance' ''')
            if cursor.fetchone()[0]==0:
                self._dbHandler.execute('''CREATE TABLE IF NOT EXISTS device_performance 
                    (ID INTEGER PRIMARY KEY   AUTOINCREMENT,
                    cpu_count INT NOT NULL,
                    cpu_percent FLOAT     NOT NULL,
                    cpu_frequency_current FLOAT NOT NULL,
                    cpu_frequency_min FLOAT NOT NULL,
                    cpu_frequency_max FLOAT NOT NULL,
                    memory_percent FLOAT NOT NULL,
                    recorded_time TEXT NOT NULL);''')
                logger.info('create table successfully')
                self._dbHandler.commit()
        except Exception as e:
            logger.error('sqlite error', e)
            return False
        return True

    def _writeTo(self, performance):
        try:
            self._dbHandler.execute('''INSERT INTO device_performance(cpu_count, cpu_percent,
                cpu_frequency_current, cpu_frequency_min, cpu_frequency_max, memory_percent, recorded_time)
                VALUES (?,?,?,?,?,?,?)''',
                [performance[0]['cpu_count'],
                performance[0]['cpu_percent'],
                performance[0]['cpu_frequency_current'],
                performance[0]['cpu_frequency_min'],
                performance[0]['cpu_frequency_max'],
                performance[0]['memory_percent'],
                performance[0]['recorded_time']])
            self._dbHandler.commit()
            # logger.info('write into DB successfully')
        except Exception as e:
            logger.error('writing DB occurs some error', e)
            return False
        return True
