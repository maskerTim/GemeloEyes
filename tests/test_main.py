import sys
import os
# add a search path for find psMonitor module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'psMonitor'))
print(sys.path)

import unittest
from psMonitor.templates.CPUMemWithInfluxDB import CPUMemWithInfluxDB
from psMonitor.templates.CPUMemWithMQTT import CPUMemWithMQTT
from psMonitor.exceptions.EmptyListError import EmptyListError
import psutil
from dotenv import load_dotenv

# load the environment test
dotenv_path = os.path.join(os.path.dirname(__file__),'.env_test')
load_dotenv(dotenv_path=dotenv_path)


class TestMonitor(unittest.TestCase):
    """ Psutil, InfluxDB, Grafana template to monitor process' CPU and Memory """

    def setUp(self) -> None:
        print ("this setUp() method called once per tests too.\n")
        self._single_process_id = [int(os.getenv('SINGLE_PROCESS_ID'))]
        self._single_process_name = [os.getenv('SINGLE_PROCESS_NAME')]
        self._multiple_process_id = [int(x) for x in os.getenv('MULTIPLE_PROCESS_ID').split(',')]
        self._multiple_process_name = os.getenv('MULTIPLE_PROCESS_NAME').split(',')
        self._noexist_process_id = [int(os.getenv('NOEXIST_PROCESS_ID'))]
        self._ps_controller_single = CPUMemWithInfluxDB(self._single_process_id)
        self._ps_controller_multiple = CPUMemWithInfluxDB(self._multiple_process_id)

    def test_monitor_CPUAndMem(self):
        """ test to monitor cpu and memory of a process """
        # Business Logic/Function
        self._ps_controller_single.getPerformance()
        self._ps_controller_multiple.getPerformance()

        # Expected
        # Expected name and ID of process are same
        for ps in self._ps_controller_single._perf:
            self.assertEqual(self._single_process_name[0], ps['tags']['name'])
            self.assertEqual(self._single_process_id[0], ps['tags']['pid'])

        sorted_lists = sorted(self._ps_controller_multiple._perf, key=lambda p:p['tags']['pid'])
        self.assertEqual(sorted_lists[0]['tags']['pid'], self._multiple_process_id[0])
        self.assertEqual(sorted_lists[0]['tags']['name'], self._multiple_process_name[0])
        self.assertEqual(sorted_lists[1]['tags']['pid'], self._multiple_process_id[1])
        self.assertEqual(sorted_lists[1]['tags']['name'], self._multiple_process_name[1])
            

    @unittest.skip("some exception can't catch")
    def test_monitor_exception(self):
        """ test error in monitoring cpu and memory of a process """
        # Setup
        ps_controller_empty = CPUMemWithInfluxDB([])

        # Expected
        # Expected the exception that list of processes is empty
        with self.assertRaises(EmptyListError) as e:
            ps_controller_empty.getPerformance()
        self.assertEqual(e.exception(), 'Error for Empty List!')
        with self.assertRaises(psutil.NoSuchProcess):
            ps_controller_noexist = CPUMemWithInfluxDB(self._noexist_process_id)

    def tearDown(self) -> None:
        print ("this teardown() method called once per tests too.\n")
        self._single_process_id = None
        self._multiple_process_id = None
        self._noexist_process_id = None
        self._single_process_name = None
        self._multiple_process_name = None
        self._ps_controller_single = None
        self._ps_controller_multiple = None

# class TestWriteDB(unittest.TestCase):

#     def setUp(self) -> None:
#         print ("this setUp() method called once per tests too.\n")
#         self._single_process_id = [int(os.getenv('SINGLE_PROCESS_ID'))]
#         self._single_process_name = [os.getenv('SINGLE_PROCESS_NAME')]
#         self._ps_controller_single = CPUMemWithInfluxDB([int(os.getenv('SINGLE_PROCESS_ID'))])
#         self._ps_controller_single.getPerformance()
#         self._ps_controller_single.connectToDB()


#     def test_write_to_DB(self):
#         """ test writing performance records into DB (in this case we take influxDB """
#         # Business Logic
#         self._ps_controller_single.writeToDB()

#         # Expected
#         # Expected the record that's written in DB is correct
#         self.assertIsNotNone(self._ps_controller_single._DBclient)
#         result = self._ps_controller_single._DBclient.query('select * from CPUandMem')
#         self.assertEqual(list(result.get_points())[0]['pid'], self._single_process_id[0])
#         self.assertEqual(list(result.get_points())[0]['name'], self._single_process_name[0])

#     def tearDown(self) -> None:
#         print ("this teardown() method called once per tests too.\n")
#         self._single_process_id = None
#         self._single_process_name = None
#         self._ps_controller_single._DBclient.query('drop measurement CPUandMem')
#         self._ps_controller_single.clearData()
#         self._ps_controller_single._DBclient.close()
#         self._ps_controller_single = None

# class TestCPUAndMemTemplate(unittest.TestCase):
#     """ Test the template pattenr of monitoring CPU and Memory """

#     def setUp(self) -> None:
#         print ("this setup() method called once per tests too.\n")
#         self._multiple_process_id = [int(x) for x in os.getenv('MULTIPLE_PROCESS_ID').split(',')]
#         self._multiple_process_name = os.getenv('MULTIPLE_PROCESS_NAME').split(',')
#         self._ps_controller_multiple = CPUMemWithInfluxDB(self._multiple_process_id)

#     def testMonitor5Times(self):
#         """ Test to monitor 5 times"""
#         # Business Logic/Functions
#         for i in range(5):
#             self._ps_controller_multiple.monitorWithDB()
        
#         # Expected
#         results = self._ps_controller_multiple._DBclient.query('select * from CPUandMem')
#         # Expected the number of results
#         self.assertEqual(len(list(results.get_points())), 10)
#         # Expected the result is correct
#         sorted_results = sorted(list(results.get_points()), key=lambda r:r['pid'])
#         index = 0
#         for result in sorted_results:
#             if index < 5:
#                 self.assertEqual(result['pid'], self._multiple_process_id[0])
#                 self.assertEqual(result['name'], self._multiple_process_name[0])
#             else:
#                 self.assertEqual(result['pid'], self._multiple_process_id[1])
#                 self.assertEqual(result['name'], self._multiple_process_name[1])
#             index+=1

#     def tearDown(self) -> None:
#         print ("this teardown() method called once per tests too.\n")
#         self._ps_controller_multiple._DBclient.query('drop measurement CPUandMem')
#         self._ps_controller_multiple._DBclient.close()
#         self._ps_controller_multiple = None

class TestSendToMQTT(unittest.TestCase):
    """ Send cpu and memory data to MQTT """
    
    def setUp(self) -> None:
        print ("this setup() method called once per tests too.\n")
        self._single_process_id = [int(os.getenv('SINGLE_PROCESS_ID'))]
        self._single_process_name = [os.getenv('SINGLE_PROCESS_NAME')]
        self._ps_controller_single = CPUMemWithMQTT([int(os.getenv('SINGLE_PROCESS_ID'))])
        self._ps_controller_single.getPerformance()
        self._ps_controller_single.connectToNetwork()

    def testWriteToNetwork(self):
        """ test that writes to network, in this case is MQTT """
        # Business Logic
        self._ps_controller_single.writeToNetwork()

        # Expected
        # Expected the record that's written in DB is correct
        self.assertIsNotNone(self._ps_controller_single._socketclient)
        # Use the mosquitto to check the message

    def tearDown(self) -> None:
        print ("this teardown() method called once per tests too.\n")
        self._single_process_id = None
        self._single_process_name = None
        self._ps_controller_single = None

class TestCPUMemMQTTTemplate(unittest.TestCase):
    """ Test the template pattern of sending cpu and memory data by MQTT """
    def setUp(self) -> None:
        print ("this setup() method called once per tests too.\n")
        self._multiple_process_id = [int(x) for x in os.getenv('MULTIPLE_PROCESS_ID').split(',')]
        self._multiple_process_name = os.getenv('MULTIPLE_PROCESS_NAME').split(',')
        self._ps_controller_multiple = CPUMemWithMQTT(self._multiple_process_id)

    def testMonitor5times(self):
        """ Test to monitor 5 times through MQTT network"""
        # Business Logic/Functions
        for i in range(5):
            self._ps_controller_multiple.monitorThroughNetwork()
        
        # Expected
        # Use the mosquitto to check the message

    def tearDown(self) -> None:
        print ("this teardown() method called once per tests too.\n")
        self._multiple_process_id = None
        self._ps_controller_multiple = None

if __name__=='__main__':
    # Run all unit test
    unittest.main(verbosity=1)