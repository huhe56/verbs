'''
Created on Oct 31, 2013

@author: huhe
'''
import unittest
import inspect

from main.define import DefineMpi
from main import define
from lib.cimc import CIMC
from lib.node_compute import NodeCompute
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
        self._logger.debug("\n\n====================== in setUp() ======================\n")
        self._host_ip_1 = TestCimcCreate.__host_ip_1
        self._host_ip_2 = TestCimcCreate.__host_ip_2
        
        self._cimc_1 = TestCimcCreate.__cimc_1
        self._cimc_2 = TestCimcCreate.__cimc_2
        
        adapter_index = 1
        self._cimc_1.delete_all_host_eth_if_from_top(adapter_index)
        self._cimc_2.delete_all_host_eth_if_from_top(adapter_index)
        
        
    def tearDown(self):
        pass
    
    
    def test_create_2pf_01usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 1   
        count = 1    
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count
                                  }
        expected_usnic_count_list = [count, count]
        
        self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: 2,
                            DefineMpi.MPI_PARAM_CHECK_VF_USED_COUNT: [1, 1]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
    
    def test_create_2pf_16usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 1   
        count = 16    
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count
                                  }
        expected_usnic_count_list = [count, count]
        
        self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        self.create_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: 32,
                            DefineMpi.MPI_PARAM_CHECK_VF_USED_COUNT: [16, 16]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
    
    
    def test_create_2pf_32usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 1   
        count = 32    
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count
                                  }
        expected_usnic_count_list = [count, count]
        
        self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        self.create_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: 32,
                            DefineMpi.MPI_PARAM_CHECK_VF_USED_COUNT: [16, 16]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        
    def test_create_2pf_64usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 1   
        count = 64   
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count
                                  }
        expected_usnic_count_list = [count, count]
        
        self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        self.create_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: 32,
                            DefineMpi.MPI_PARAM_CHECK_VF_USED_COUNT: [16, 16]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
     
    
   
        
    
    def test_create_2pf_diff_usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = 1   
        usnic_count_dictionary = {
                                "eth0": 65,
                                "eth1": 19
                                  }
        expected_usnic_count_list = [65, 19]
        self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: 32,
                            DefineMpi.MPI_PARAM_CHECK_VF_USED_COUNT: [16, 16]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
    
    
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
        
        ''' need to change for each server pair '''
        host_if_ip_dictionary_1 = {
                                 "eth8": "50.35.50.113/24",
                                 "eth9": "50.35.60.113/24",
                                 }
        host_if_ip_dictionary_2 = {
                                 "eth8": "50.35.50.114/24",
                                 "eth9": "50.35.60.114/24",
                                 }
        
        self.create_pf_and_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, host_eth_if_dictionary, usnic_count_dictionary, expected_usnic_count_list, host_if_ip_dictionary_1)
        self.create_pf_and_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, host_eth_if_dictionary, usnic_count_dictionary, expected_usnic_count_list, host_if_ip_dictionary_2)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: 32,
                            DefineMpi.MPI_PARAM_CHECK_VF_USED_COUNT: [16, 16]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    #suite = unittest.TestLoader().loadTestsFromTestCase(HostDriverTest)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    
    