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
from lib.node_compute import NodeCompute
from main.test_base import TestBase
from utils.utils import Utils


class TestCimcCreate(unittest.TestCase, TestBase):

    @classmethod
    def setUpClass(cls):
        pass
    
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    
    def setUp(self):
        define.PEXPECT_OUTPUT_STDOUT = False
        
        self._host_1 = DefineMpi.NODE_HOST_IP_1
        self._cimc_1 = CIMC(DefineMpi.NODE_CIMC_IP_1)        
        TestBase.init(self, self._cimc_1.get_ssh())
        
        
    def tearDown(self):
        self._cimc_1._ssh.exit()
        Utils.append_file(Define.PATH_USNIC_LOG_FILE_ALL, Define.PATH_USNIC_LOG_FILE)

    
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
        
    
    def test_create_2pf_16usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 1   
        count = 16    
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count
                                  }
        expected_usnic_count_list = [count, count]
        
        self.create_usnic(self._cimc_1, adapter_index, usnic_count_dictionary)
        self.check_host_usnic(self._host_1, expected_usnic_count_list)
        
        self._host_2 = DefineMpi.NODE_HOST_IP_2
        self._cimc_2 = CIMC(DefineMpi.NODE_CIMC_IP_2)      
        self.create_usnic(self._cimc_2, adapter_index, usnic_count_dictionary)
        self.check_host_usnic(self._host_2, expected_usnic_count_list)
        
        self.run_mpi(self._host_1)
        
    
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
     
    
    def test_create_2pf_32usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 1   
        count = 32    
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count
                                  }
        expected_usnic_count_list = [count, count]
        
        self.create_usnic(self._cimc_1, adapter_index, usnic_count_dictionary)
        self.check_host_usnic(self._host_1, expected_usnic_count_list)
        
        self.run_mpi(self._host_1)
        
    
    def test_create_2pf_diff_usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 2   
        usnic_count_dictionary = {
                                "eth0": 65,
                                "eth1": 19
                                  }
        expected_usnic_count_list = [-1, -1, 65, 19]
        
        self.create_usnic(self._cimc_1, adapter_index, usnic_count_dictionary)
        self.check_host_usnic(self._host_1, expected_usnic_count_list)
        
        self.run_mpi(self._host_1)
    
    
    def test_create_4pf_16usnic(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 1
        count = 16
        host_eth_if_dictionary = {
                                "eth2": {"uplink": 0, "vlan": 50, "vlan-mode": "trunk"}, 
                                "eth3": {"uplink": 0, "vlan": 60, "vlan-mode": "trunk"}
                                }
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count,
                                "eth2": count,
                                "eth3": count
                                  }
        expected_usnic_count_list = [count, count, count, count]
                                                
        self.create_pf(self._cimc_1, adapter_index, host_eth_if_dictionary)
        self.create_usnic(self._cimc_1, adapter_index, usnic_count_dictionary)
        self.check_host_usnic(self._host_1, expected_usnic_count_list)
        
        self._cimc_1.delete_all_host_eth_if_from_top(adapter_index)
        
        
    def test_create_16pf_14usnic(self):        
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 1
        count = 13
        
        new_host_eth_if_list = ["eth" + str(i) for i in range(2, 16)]
        
        for host_eth_if in new_host_eth_if_list:
            self._cimc_1.create_host_eth_if_from_top(adapter_index, host_eth_if)
        
        host_eth_if_list = Define.CIMC_DEFAULT_ETH_IF_LIST + new_host_eth_if_list
        self.create_same_usnic(adapter_index, host_eth_if_list, count)
        
        self._cimc_1.power_cycle()
        
        node = Util.wait_for_node_to_boot_up(self._host_1)
        usnic_configured_count_list = node.get_usnic_configured_count_list()        
        expected_usnic_configured_count_list = [count for i in range(0, 18)]
        self.assertEqual(usnic_configured_count_list, expected_usnic_configured_count_list)
        
        self._cimc_1.delete_all_host_eth_if_from_top(adapter_index)
    
        
    def create_pf(self, cimc, adapter_index, host_eth_if_dictionary):
        cimc.create_host_eth_if_from_top(cimc, adapter_index, host_eth_if_dictionary)
        
        
    def create_usnic(self, cimc, adapter_index, usnic_count_dictionary):
        for host_eth_if, usnic_count in usnic_count_dictionary.iteritems():
            cimc.create_usnic_from_top(adapter_index, host_eth_if, usnic_count)
            created_usnic_count = cimc.get_usnic_count()
            self.assertEqual(created_usnic_count, usnic_count)
        cimc.power_cycle()
        
    
    def check_host_usnic(self, host, expected_usnic_count_list):
        host = Util.wait_for_node_to_boot_up(host)
        configured_usnic_count_list = host.get_usnic_configured_count_list()        
        for configured_count, expected_count in zip(configured_usnic_count_list, expected_usnic_count_list):
            if expected_count > 0:
                self.assertEqual(configured_count, expected_count)
        return host
        
        
    def run_mpi(self, host):
        host = NodeCompute(host)
        ret = host.run_mpi(DefineMpi.MPI_CMD_PINGPONG, DefineMpi.MPI_CMD_TIMEOUT_PINGPONG)
        self.assertEquals(ret, 0)
        shell_status = host.get_shell_status()
        self.assertEqual(shell_status, 0)
        
    
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
        
        
    def delete_non_default_host_eth_if(self, cimc, adapter_index):
        cimc.scope_adapter_from_top(adapter_index)
        cimc.delete_all_host_eth_if()
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    #suite = unittest.TestLoader().loadTestsFromTestCase(HostDriverTest)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    
    