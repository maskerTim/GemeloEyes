import sys
import os

import psutil
# add a search path for find psMonitor module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'psMonitor'))
print(sys.path)

import unittest
import psutil
from psMonitor.templates.deviceMonitor.CPUandMemoryForDM import CPUandMemoryForDM
from dotenv import load_dotenv
import sqlite3

# load the environment test
dotenv_path = os.path.join(os.path.dirname(__file__),'.env_test')
load_dotenv(dotenv_path=dotenv_path)

class TestDeviceMonitor(unittest.TestCase):
    """ Device Monitor for monitoring CPU and memory """

    def setUp(self) -> None:
        """ this setUp() method called once per tests too """
        self._deviceMonitor = CPUandMemoryForDM()

    def test_getPerformance_CPUAndMem(self):
        """ test to monitor device's cpu and memory """
        # Business Logic/Function
        result = self._deviceMonitor.test_monitor('getPerformance')

        # Expected
        # Expected CPU and memory information
        self.assertEqual(result[0]['cpu_count'], 4)

    def test_writeTo_DB(self):
        """ test to write to Database (in this case is sqlite) """
        # Business Logic/Function
        self._deviceMonitor.test_monitor('getPerformance')
        self._deviceMonitor.test_monitor('writeTo')

        # Expected
        # Expected write into DB
        conn = sqlite3.connect('performance.db')
        cursor = conn.execute("SELECT cpu_count, cpu_percent from device_performance")
        for row in cursor:
            self.assertEqual(row[0], 4)
        conn.close()

    def test_monitor_CPUandMem(self):
        """ test device monitor run one time"""
        # Business Logic/Function
        self._deviceMonitor.monitor()

        # Expected
        # Expected the monitoring succeeds to run
        conn = sqlite3.connect('performance.db')
        cursor = conn.execute("SELECT cpu_count, cpu_percent from device_performance")
        for row in cursor:
            self.assertEqual(row[0], 4)
        conn.close()

    def tearDown(self) -> None:
        """ this teardown() method called once per tests too """
        pass

if __name__=='__main__':
    # Run all unit test
    unittest.main(verbosity=1)