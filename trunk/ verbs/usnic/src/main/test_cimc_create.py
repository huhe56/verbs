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

    '''
    @unittest.skip    
    def test_create_1pf_usnic_default_host_eth_if(self):
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
    
    
    
    def test_create_1pf_usnic_max_default_host_eth_if_negative(self):
        self.init_test(inspect.stack()[0][3])
        test_type = False
        
        ### remove usnic from eth1 
        adapter_index = 1        
        host_eth_if = "eth1"
        self._cimc_1.delete_usnic_from_top(adapter_index, host_eth_if)
        
        host_eth_if = "eth0"
        count = Define.CIMC_MAX_USNIC_PER_ADAPTER + 1
        self.check_set_usnic(adapter_index, host_eth_if, count, test_type)
        
        
    def test_create_1pf_usnic_string_default_host_eth_if_negative(self):
        self.init_test(inspect.stack()[0][3])
        test_type = False
        
        ### remove usnic from eth1 
        adapter_index = 1        
        host_eth_if = "eth1"
        self._cimc_1.delete_usnic_from_top(adapter_index, host_eth_if)
        
        host_eth_if = "eth0"
        count = "wrong"
        self.check_set_usnic(adapter_index, host_eth_if, count, test_type)
        
        
    def test_create_1pf_usnic_minus_default_host_eth_if_negative(self):
        self.init_test(inspect.stack()[0][3])
        test_type = False
        
        ### remove usnic from eth1 
        adapter_index = 1        
        host_eth_if = "eth1"
        self._cimc_1.delete_usnic_from_top(adapter_index, host_eth_if)
        
        host_eth_if = "eth0"
        count = "-1"
        self.check_set_usnic(adapter_index, host_eth_if, count, test_type)
        
    
    @unittest.skip 
    def test_create_2pf_usnic_default_host_eth_if(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 1   
        count = 16    
         
        for host_eth_if in Define.CIMC_DEFAULT_ETH_IF_LIST:
            self._cimc_1.create_usnic_from_top(adapter_index, host_eth_if, count)
            self.check_create_usnic(adapter_index, host_eth_if, count)
        

        for host_eth_if in Define.CIMC_DEFAULT_ETH_IF_LIST:
            count = Define.CIMC_MAX_USNIC_2PF_LIST[host_eth_if]
            self.check_set_usnic(adapter_index, host_eth_if, count)
        
        
    @unittest.skip
    def test_create_2pf_usnic_max_default_host_eth_if_negative(self):
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
    
        
    @unittest.skip 
    def test_create_2pf_16usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        count = 16
        self.run_create_2pf_same_usnic_run_mpi(count)
        
        
    @unittest.skip 
    def test_create_2pf_32usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        count = 32
        self.run_create_2pf_same_usnic_run_mpi(count)
    '''
        
    def test_create_4pf_16usnic(self):
        adapter_index = 1
        count = 16
        
        new_host_eth_if_list = ["eth2", "eth3"]
        
        for host_eth_if in new_host_eth_if_list:
            self._cimc_1.create_host_eth_if_from_top(adapter_index, host_eth_if)
        
        adapter_index_list = [adapter_index]
        host_eth_if_list = Define.CIMC_DEFAULT_ETH_IF_LIST + new_host_eth_if_list
        self.create_same_usnic(adapter_index_list, host_eth_if_list, count)
        
        self._cimc_1.delete_all_host_eth_if_from_top(adapter_index)
    
    '''
    def test_create_16pf_14usnic(self):        
        adapter_index = 1
        count = 14
        
        new_host_eth_if_list = ["eth" + str(i) for i in range(2, 16)]
        
        for host_eth_if in new_host_eth_if_list:
            self._cimc_1.create_host_eth_if_from_top(adapter_index, host_eth_if)
        
        adapter_index_list = [adapter_index]
        host_eth_if_list = Define.CIMC_DEFAULT_ETH_IF_LIST + new_host_eth_if_list
        self.create_same_usnic(adapter_index_list, host_eth_if_list, count)
        
        self._cimc_1.power_cycle()
        
        node = Util.wait_for_node_to_boot_up(self._host_1)
        usnic_configured_count_list = node.get_usnic_configured_count_list()        
        expected_usnic_configured_count_list = [count for i in range(0, 18)]
        self.assertEqual(usnic_configured_count_list, expected_usnic_configured_count_list)
        
        self._cimc_1.delete_all_host_eth_if_from_top(adapter_index)
    '''
    
    def create_same_usnic(self, adapter_index_list, host_eth_if_list, count):
        for adapter_index in adapter_index_list:
            for host_eth_if in host_eth_if_list:
                self._cimc_1.create_usnic_from_top(adapter_index, host_eth_if, count)
                self.check_create_usnic(adapter_index, host_eth_if, count)
                
        
    def run_create_2pf_same_usnic_run_mpi(self, count):
        for adapter_index in [1, 2]:
            for host_eth_if in Define.CIMC_DEFAULT_ETH_IF_LIST:
                self._cimc_1.create_usnic_from_top(adapter_index, host_eth_if, count)
                self.check_create_usnic(adapter_index, host_eth_if, count)
        
        self._cimc_1.power_cycle()
        
        node = Util.wait_for_node_to_boot_up(self._host_1)
        usnic_configured_count_list = node.get_usnic_configured_count_list()        
        expected_usnic_configured_count_list = [count, count, count, count]
        self.assertEqual(usnic_configured_count_list, expected_usnic_configured_count_list)
        
        ret = node.run_mpi(DefineMpi.MPI_CMD_PINGPONG, DefineMpi.MPI_CMD_TIMEOUT_PINGPONG)
        self.assertEquals(ret, 0)
        shell_status = node.get_shell_status()
        self.assertEqual(shell_status, 0)
        
        
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
    
    
    