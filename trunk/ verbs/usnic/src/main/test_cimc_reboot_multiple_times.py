'''
Created on Oct 31, 2013

@author: huhe
'''
import time
import unittest
import inspect

from main.define import Define, DefineMpi
from main import define
from lib.cimc import CIMC
from lib.util import Util
from lib.node_compute import NodeCompute
from main.test_base import TestBase


class TestCimcReboot(unittest.TestCase, TestBase):

    @classmethod
    def setUpClass(cls):
        define.PEXPECT_OUTPUT_STDOUT = False
        TestCimcReboot.__host_ip_1 = DefineMpi.NODE_HOST_IP_1
        TestCimcReboot.__host_ip_2 = DefineMpi.NODE_HOST_IP_2
        TestCimcReboot.__cimc_1 = CIMC(DefineMpi.NODE_CIMC_IP_1)  
        TestCimcReboot.__cimc_2 = CIMC(DefineMpi.NODE_CIMC_IP_2)
    
        TestCimcReboot.__cimc_1_adapter_index_list = TestCimcReboot.__cimc_1.get_adapter_index_list_from_top()
        TestCimcReboot.__cimc_2_adapter_index_list = TestCimcReboot.__cimc_2.get_adapter_index_list_from_top()
        
    
    @classmethod
    def tearDownClass(cls):
        TestCimcReboot.__cimc_1._ssh.exit()
        TestCimcReboot.__cimc_2._ssh.exit()
    
    
    def setUp(self):
        TestBase.init(self)
        #self._logger.debug("\n\n====================== in setUp() ======================")
        self._host_ip_1 = TestCimcReboot.__host_ip_1
        self._host_ip_2 = TestCimcReboot.__host_ip_2
        
        self._cimc_1 = TestCimcReboot.__cimc_1
        self._cimc_2 = TestCimcReboot.__cimc_2
        
        self._cimc_1.show_cimc_detail()
        self._cimc_2.show_cimc_detail()
        
        self._cimc_1_adapter_index_list = TestCimcReboot.__cimc_1_adapter_index_list
        self._cimc_2_adapter_index_list = TestCimcReboot.__cimc_2_adapter_index_list
        
        self._cimc_1_adapter_count = len(self._cimc_1_adapter_index_list)
        self._cimc_2_adapter_count = len(self._cimc_2_adapter_index_list)
        
        for adapter_index in self._cimc_1_adapter_index_list:
            self._cimc_1.delete_all_host_eth_if_from_top(adapter_index)
        for adapter_index in self._cimc_2_adapter_index_list:
            self._cimc_2.delete_all_host_eth_if_from_top(adapter_index)
        
        
    def tearDown(self):
        self.finish_test()

        
    def test_reboot_1(self):
        self.init_test(inspect.stack()[0][3])
        usnic_count = 16
        self.reboot_test(self._cimc_1, self._host_ip_1, usnic_count)
        
    
    def test_reboot_2(self):
        self.init_test(inspect.stack()[0][3])
        usnic_count = 16
        self.reboot_test(self._cimc_2, self._host_ip_2, usnic_count)
    
        
    def reboot_test(self, cimc, host_ip, usnic_count):
        
        for i in range(5):
            cimc.power_cycle()
            Util.wait_for_node_to_boot_up(host_ip)
            time.sleep(30)
        
        self.prepare_and_run_mpi(host_ip, usnic_count)
    
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    #suite = unittest.TestLoader().loadTestsFromTestCase(HostDriverTest)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    
    