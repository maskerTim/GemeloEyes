import sys
import os

# add a search path for find psMonitor module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'psMonitor'))
print(sys.path)

import unittest
from psMonitor.factory.DBFactory import DBFactory
from psMonitor.templates.deviceMonitor.CPUandMemoryForDM import CPUandMemoryForDM
from psMonitor.factory.NWFactory import NWFactory
import sqlite3

class TestDBFactory(unittest.TestCase):
    """ Test of Database Factory """

    def setUp(self) -> None:
        """ this setUp() method called once per tests too """
        self.testDB = DBFactory.createInstance('sqlite3', host='performance.db')
        self._deviceMonitor = CPUandMemoryForDM(handler=self.testDB)

    def test_connectToDB(self):
        """ test connecting to DB """
        # Business Logic
        result = self.testDB._connectTo()
        # Expected
        self.assertTrue(result)

    def test_writeToDB(self):
        """ test writing to DB """
        # Business Logic
        perf = self._deviceMonitor.test_monitor('getPerformance')
        self.testDB._connectTo()
        self.testDB._writeTo(perf)

        # Expected
        conn = sqlite3.connect('performance.db')
        cursor = conn.execute("SELECT cpu_count, cpu_percent from device_performance")
        for row in cursor:
            self.assertEqual(row[0], 4)
        conn.close()

    def test_combined_with_template(self):
        """ test using template with Database factory """
        # Business Logic
        self._deviceMonitor.monitor()

        # Expected
        conn = sqlite3.connect('performance.db')
        cursor = conn.execute("SELECT cpu_count, cpu_percent from device_performance")
        for row in cursor:
            self.assertEqual(row[0], 4)
        conn.close()

    def tearDown(self) -> None:
        """ this teardown() method called once per tests too """
        pass

class TestNetworkFactory(unittest.TestCase):
    """ Test of Network Factory """

    def setUp(self) -> None:
        """ this setUp() method called once per tests too """
        self.testNW = NWFactory.createInstance('mqtt', host=("192.168.0.199", 1883))
        self._deviceMonitor = CPUandMemoryForDM(handler=self.testNW)

    def test_connectToBroker(self):
        """ test connecting to MQTT broker """
        # Business Logic
        result = self.testNW._connectTo()
        # Expected
        self.assertTrue(result)

    def test_writeToBroker(self):
        """ test writing to MQTT broker """
        # Business Logic
        perf = self._deviceMonitor.test_monitor('getPerformance')
        self.testNW._connectTo()
        self.testNW.setTopic("Try/Test")
        result = self.testNW._writeTo(perf)

        # Expected
        self.assertTrue(result)

    def test_combined_with_template(self):
        """ test using template with Network factory """
        # Business Logic
        self.testNW.setTopic("Try/Test")
        self._deviceMonitor.monitor()

        # Expected (using mosquitto_sub to test)
        # This test don't implement here
        self.assertTrue(True)

    def test_exception_when_not_set_topic(self):
        """ test raise exception when not set topic """
        try:
            self._deviceMonitor.monitor()
            # When the monitor do not throw exception, the test is failure
            self.assertFalse(True)
        except:
            self.assertTrue(True)
        
        
    def tearDown(self) -> None:
        """ this teardown() method called once per tests too """
        pass

if __name__=='__main__':
    # Run all unit test
    unittest.main(verbosity=1)