import sys
import os
# add a search path for find psMonitor module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'psMonitor'))
print(sys.path)

import unittest
from psMonitor.templates.CPUMemTemplate import CPUMemTemplate
from psMonitor.exceptions.EmptyListError import EmptyListError
import psutil
from dotenv import load_dotenv

# load the environment test
dotenv_path = os.path.join(os.path.dirname(__file__),'.env_test')
load_dotenv(dotenv_path=dotenv_path)


class TestMonitor(unittest.TestCase):
    """ Psutil, InfluxDB, Grafana template to monitor process' CPU and Memory """

    @classmethod
    def setUpClass(cls) -> None:
        print ("this setupclass() method only called once.\n")

    def test_monitor_CPUAndMem(self):
        """ test to monitor cpu and memory of a process """
        # Setup
        single_process_id = [16098]
        ps_controller_single = CPUMemTemplate(single_process_id)
        multiple_process_ids = [16098, 13380]
        ps_controller_multiple = CPUMemTemplate(multiple_process_ids)

        # Business Logic/Function
        ps_controller_single.getPerformance()
        ps_controller_multiple.getPerformance()

        # Expected
        # Expected name and ID of process are same
        for ps in ps_controller_single._perf:
            self.assertEqual('top', ps['tags']['name'])
            self.assertEqual(16098, ps['tags']['pid'])

        sorted_lists = sorted(ps_controller_multiple._perf, key=lambda p:p['tags']['pid'])
        self.assertEqual(sorted_lists[0]['tags']['pid'], 13380)
        self.assertEqual(sorted_lists[0]['tags']['name'], 'xrdp')
        self.assertEqual(sorted_lists[1]['tags']['pid'], 16098)
        self.assertEqual(sorted_lists[1]['tags']['name'], 'top')
            

    def test_monitor_exception(self):
        """ test error in monitoring cpu and memory of a process """
        # Setup
        empty_process_ids = []
        ps_controller_empty = CPUMemTemplate(empty_process_ids)
        error_process_ids = [1111]
        
        # Expected
        # Expected the exception that list of processes is empty
        with self.assertRaises(EmptyListError):
            ps_controller_empty.getPerformance()
        with self.assertRaises(psutil.NoSuchProcess):
            ps_controller_error = CPUMemTemplate(error_process_ids)

    @classmethod
    def tearDownClass(cls) -> None:
        print ("this teardownclass() method only called once too.\n")

class TestWriteDB(unittest.TestCase):
    ps_controller_single = None

    @classmethod
    def setUpClass(cls) -> None:
        print ("this setupclass() method only called once.\n")
        single_process_id = [16098]
        cls.ps_controller_single = CPUMemTemplate(single_process_id)
        cls.ps_controller_single.getPerformance()
        cls.ps_controller_single.connectToDB()


    def test_write_to_DB(self):
        """ test writing performance records into DB (in this case we take influxDB """
        # Business Logic
        self.ps_controller_single.writeToDB()

        # Expected
        # Expected the record that's written in DB is correct
        self.assertIsNotNone(self.ps_controller_single._DBclient)
        result = self.ps_controller_single._DBclient.query('select * from CPUandMem')
        self.assertEqual(list(result.get_points())[0]['pid'], '16098')
        self.assertEqual(list(result.get_points())[0]['name'], 'top')

    @classmethod
    def tearDownClass(cls) -> None:
        print ("this teardownclass() method only called once too.\n")
        cls.ps_controller_single._DBclient.query('drop measurement CPUandMem')
        cls.ps_controller_single.clearData()
        cls.ps_controller_single._DBclient.close()

class TestCPUAndMemTemplate(unittest.TestCase):
    """ Test the template pattenr of monitoring CPU and Memory """
    ps_controller_multiple = None

    @classmethod
    def setUpClass(cls) -> None:
        print ("this setupclass() method only called once.\n")
        multiple_process_id = [16098, 13380]
        cls.ps_controller_multiple = CPUMemTemplate(multiple_process_id)

    def testMonitor5Times(self):
        """ Test to monitor 5 times"""
        # Business Logic/Functions
        for i in range(5):
            self.ps_controller_multiple.monitor()
        
        # Expected
        results = self.ps_controller_multiple._DBclient.query('select * from CPUandMem')
        # Expected the number of results
        self.assertEqual(len(list(results.get_points())), 10)
        # Expected the result is correct
        sorted_results = sorted(list(results.get_points()), key=lambda r:r['pid'])
        index = 0
        for result in sorted_results:
            if index < 5:
                self.assertEqual(result['pid'], '13380')
                self.assertEqual(result['name'], 'xrdp')
            else:
                self.assertEqual(result['pid'], '16098')
                self.assertEqual(result['name'], 'top')
            index+=1

    @classmethod
    def tearDownClass(cls) -> None:
        print ("this teardownclass() method only called once too.\n")
        cls.ps_controller_multiple._DBclient.query('drop measurement CPUandMem')
        cls.ps_controller_multiple._DBclient.close()

if __name__=='__main__':
    # Run all unit test
    unittest.main(verbosity=1)