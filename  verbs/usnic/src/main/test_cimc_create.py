'''
Created on Oct 31, 2013

@author: huhe
'''
import unittest
import inspect

from main.define import Define, DefineMpi
from main import define
from lib.cimc import CIMC
from lib.util import Util
from main.test_base import TestBase


class TestCimcCreate(unittest.TestCase, TestBase):

    @classmethod
    def setUpClass(cls):
        define.PEXPECT_OUTPUT_STDOUT = False
        TestCimcCreate.__host_ip_1 = DefineMpi.NODE_HOST_IP_1
        TestCimcCreate.__host_ip_2 = DefineMpi.NODE_HOST_IP_2
        TestCimcCreate.__cimc_1 = CIMC(DefineMpi.NODE_CIMC_IP_1)  
        TestCimcCreate.__cimc_2 = CIMC(DefineMpi.NODE_CIMC_IP_2)
    
    
    @classmethod
    def tearDownClass(cls):
        TestCimcCreate.__cimc_1._ssh.exit()
    
    
    def setUp(self):
        TestBase.init(self)
        self._logger.debug("\n\n====================== in setUp() ======================")
        self._host_ip_1 = TestCimcCreate.__host_ip_1
        self._host_ip_2 = TestCimcCreate.__host_ip_2
        
        self._cimc_1 = TestCimcCreate.__cimc_1
        self._cimc_2 = TestCimcCreate.__cimc_2
        
        adapter_index = 1
        self._cimc_1.delete_all_host_eth_if_from_top(adapter_index)
        self._cimc_2.delete_all_host_eth_if_from_top(adapter_index)
        
        
    def tearDown(self):
        pass

    
    def test_create_1pf_usnic(self):
        self.init_test(inspect.stack()[0][3])
        
        # remove usnic from eth1 
        adapter_index = 1        
        host_eth_if = "eth1"
        self._cimc_1.delete_usnic_from_top(adapter_index, host_eth_if)
        
        adapter_index = 1        
        host_eth_if = "eth0"
        count = 1
        self.check_set_usnic(adapter_index, host_eth_if, count)
        
        count = 32
        self.check_set_usnic(adapter_index, host_eth_if, count)
        
        count = Define.CIMC_MAX_USNIC_PER_ADAPTER
        self.check_set_usnic(adapter_index, host_eth_if, count)
    
        count = 16
        self.check_set_usnic(adapter_index, host_eth_if, count)
    
    
    def test_create_1pf_usnic_max_negative(self):
        self.init_test(inspect.stack()[0][3])
        test_type = False
        
        ### remove usnic from eth1 
        adapter_index = 1        
        host_eth_if = "eth1"
        self._cimc_1.delete_usnic_from_top(adapter_index, host_eth_if)
        
        host_eth_if = "eth0"
        count = Define.CIMC_MAX_USNIC_PER_ADAPTER + 1
        self.check_set_usnic(adapter_index, host_eth_if, count, test_type)
        
    
    def test_create_1pf_usnic_string_negative(self):
        self.init_test(inspect.stack()[0][3])
        test_type = False
        
        ### remove usnic from eth1 
        adapter_index = 1        
        host_eth_if = "eth1"
        self._cimc_1.delete_usnic_from_top(adapter_index, host_eth_if)
        
        host_eth_if = "eth0"
        count = "wrong"
        self.check_set_usnic(adapter_index, host_eth_if, count, test_type)
        
    
    def test_create_1pf_usnic_minus_negative(self):
        self.init_test(inspect.stack()[0][3])
        test_type = False
        
        ### remove usnic from eth1 
        adapter_index = 1        
        host_eth_if = "eth1"
        self._cimc_1.delete_usnic_from_top(adapter_index, host_eth_if)
        
        host_eth_if = "eth0"
        count = "-1"
        self.check_set_usnic(adapter_index, host_eth_if, count, test_type)
        
    
    def test_create_2pf_usnic_max_negative(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 1   
        count = 1    
        
        for host_eth_if in Define.CIMC_DEFAULT_ETH_IF_LIST:
            self._cimc_1.create_usnic_from_top(adapter_index, host_eth_if, count)
            self.check_create_usnic(adapter_index, host_eth_if, count)
        
        count = 113
        host_eth_if = "eth0"
        self.check_set_usnic(adapter_index, host_eth_if, count)
        host_eth_if = "eth1"
        self.check_set_usnic(adapter_index, host_eth_if, count, False)
    
    
    def test_create_max16pf_13usnic(self):        
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 1
        count = 13
        
        host_eth_if_dictionary = {}
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count,
                                  }
        expected_usnic_count_list = [count, count]
        
        for i in range(2, 16):
            uplink = i % 2
            host_eth_if_dictionary["eth" + str(i)] = {"uplink": uplink, "vlan": 50, "vlan-mode": "trunk"}
            usnic_count_dictionary["eth" + str(i)] = count
            expected_usnic_count_list.append(count)
        
        self.create_pf(self._cimc_1, adapter_index, host_eth_if_dictionary)
        self._cimc_1.power_cycle()
        node_1 = Util.wait_for_node_to_boot_up(self._host_ip_1)
        self.check_host_usnic(node_1, expected_usnic_count_list)
    
    
    def create_same_usnic(self, adapter_index, host_eth_if_list, count):
        for host_eth_if in host_eth_if_list:
            self._cimc_1.create_usnic_from_top(adapter_index, host_eth_if, count)
            self.check_create_usnic(adapter_index, host_eth_if, count)
        
        
    def check_create_usnic(self, adapter_index, host_eth_if, count, test_type=True):
        self._cimc_1.scope_usnic_from_top(adapter_index, host_eth_if)
        actual_count = self._cimc_1.get_usnic_count()
        if test_type:
            self.assertEqual(count, actual_count)
        else:
            self.assertNotEqual(count, actual_count)
            
        
    def check_set_usnic(self, adapter_index, host_eth_if, count, test_type=True):
        self._cimc_1.scope_usnic_from_top(adapter_index, host_eth_if)
        self._cimc_1.set_usnic_count(count)
        actual_count = self._cimc_1.get_usnic_count()
        if test_type:
            self.assertEqual(count, actual_count)
        else:
            self.assertNotEqual(count, actual_count)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    #suite = unittest.TestLoader().loadTestsFromTestCase(HostDriverTest)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    
    