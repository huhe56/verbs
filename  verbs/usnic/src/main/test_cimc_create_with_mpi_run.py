'''
Created on Oct 31, 2013

@author: huhe
'''
import unittest
import inspect

from main.define import DefineMpi, Define
from main import define
from lib.util import Util
from lib.cimc import CIMC
from lib.node_compute import NodeCompute
from main.test_base import TestBase


class TestCimcCreateMpi(unittest.TestCase, TestBase):

    @classmethod
    def setUpClass(cls):
        define.PEXPECT_OUTPUT_STDOUT = False
        TestCimcCreateMpi.__host_ip_1 = DefineMpi.NODE_HOST_IP_1
        TestCimcCreateMpi.__host_ip_2 = DefineMpi.NODE_HOST_IP_2
        TestCimcCreateMpi.__cimc_1 = CIMC(DefineMpi.NODE_CIMC_IP_1)  
        TestCimcCreateMpi.__cimc_2 = CIMC(DefineMpi.NODE_CIMC_IP_2)
            
        TestCimcCreateMpi.__cimc_1_adapter_index_list = TestCimcCreateMpi.__cimc_1.get_adapter_index_list_from_top()
        TestCimcCreateMpi.__cimc_2_adapter_index_list = TestCimcCreateMpi.__cimc_2.get_adapter_index_list_from_top()
        
    
    @classmethod
    def tearDownClass(cls):
        TestCimcCreateMpi.__cimc_1._ssh.exit()
    
    
    def setUp(self):
        TestBase.init(self)
        self._logger.debug("\n\n====================== in setUp() ======================\n")
        self._host_ip_1 = TestCimcCreateMpi.__host_ip_1
        self._host_ip_2 = TestCimcCreateMpi.__host_ip_2
        
        self._cimc_1 = TestCimcCreateMpi.__cimc_1
        self._cimc_2 = TestCimcCreateMpi.__cimc_2
        
        self._cimc_1_adapter_index_list = TestCimcCreateMpi.__cimc_1_adapter_index_list
        self._cimc_2_adapter_index_list = TestCimcCreateMpi.__cimc_2_adapter_index_list
        
        self._cimc_1_adapter_count = len(self._cimc_1_adapter_index_list)
        self._cimc_2_adapter_count = len(self._cimc_2_adapter_index_list)
        
        
        for adapter_index in self._cimc_1_adapter_index_list:
            self._cimc_1.delete_all_host_eth_if_from_top(adapter_index)
        for adapter_index in self._cimc_2_adapter_index_list:
            self._cimc_2.delete_all_host_eth_if_from_top(adapter_index)
        
        
    def tearDown(self):
        pass
    
    
    def test_create_1pf_16usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = self._cimc_1_adapter_index_list[0]        
        host_eth_if = "eth1"
        self._cimc_1.delete_usnic_from_top(adapter_index, host_eth_if)
        self._cimc_2.delete_usnic_from_top(adapter_index, host_eth_if)
        
        if self._cimc_1_adapter_count == 2:
            adapter_index = self._cimc_1_adapter_index_list[1]
            for host_eth_if in Define.CIMC_DEFAULT_ETH_IF_LIST:
                self._cimc_1.delete_usnic_from_top(adapter_index, host_eth_if)
                self._cimc_2.delete_usnic_from_top(adapter_index, host_eth_if)
        
        
        adapter_index = self._cimc_1_adapter_index_list[0]   
        count = 16    
        usnic_count_dictionary = {
                                "eth0": count,
                                  }
        expected_usnic_count_list = [count]
        
        self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        self.create_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        np = self.calculate_max_number_of_process(Define.CIMC_CORE_PER_NODE, count, DefineMpi.NODE_NUMBER)
        nvf = np/DefineMpi.NODE_NUMBER
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [nvf]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
    
    def test_create_2pf_01usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = self._cimc_1_adapter_index_list[0]   
        count = 1    
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count
                                  }
        expected_usnic_count_list = [count, count]
        
        self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        self.create_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_CMD: DefineMpi.MPI_CMD_ALL,
                            DefineMpi.MPI_PARAM_NP: 2,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [1, 1]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        
    def test_create_2pf_08usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        count = 8
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count
                                  }
        
        expected_usnic_count_list = []
        for adapter_index in self._cimc_1_adapter_index_list:
            expected_usnic_count_list.extend([count, count])
            self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        expected_usnic_count_list = []
        for adapter_index in self._cimc_2_adapter_index_list:
            expected_usnic_count_list.extend([count, count])
            self.create_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        np = self.calculate_max_number_of_process(Define.CIMC_CORE_PER_NODE, count, DefineMpi.NODE_NUMBER)
        nvf = np/DefineMpi.NODE_NUMBER
        expected_vf_used_count_list = [nvf, nvf]
        if self._cimc_1_adapter_count == 2:
            expected_vf_used_count_list = [nvf, nvf, nvf, nvf]
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: expected_vf_used_count_list
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
    
    
    
    def test_create_2pf_16usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        count = 16    
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count
                                  }
        
        expected_usnic_count_list = []
        for adapter_index in self._cimc_1_adapter_index_list:
            expected_usnic_count_list.extend([count, count])
            self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        expected_usnic_count_list = []
        for adapter_index in self._cimc_2_adapter_index_list:
            expected_usnic_count_list.extend([count, count])
            self.create_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        np = self.calculate_max_number_of_process(Define.CIMC_CORE_PER_NODE, count, DefineMpi.NODE_NUMBER)
        nvf = np/DefineMpi.NODE_NUMBER
        expected_vf_used_count_list = [nvf, nvf]
        if self._cimc_1_adapter_count == 2:
            expected_vf_used_count_list = [nvf, nvf, nvf, nvf]
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: expected_vf_used_count_list
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
    
    
    def test_create_2pf_32usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        count = 32
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count
                                  }
        expected_usnic_count_list = []
        for adapter_index in self._cimc_1_adapter_index_list:
            expected_usnic_count_list.extend([count, count])
            self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        expected_usnic_count_list = []
        for adapter_index in self._cimc_2_adapter_index_list:
            expected_usnic_count_list.extend([count, count])
            self.create_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        np = self.calculate_max_number_of_process(Define.CIMC_CORE_PER_NODE, count, DefineMpi.NODE_NUMBER)
        nvf = np/DefineMpi.NODE_NUMBER
        expected_vf_used_count_list = [nvf, nvf]
        if self._cimc_1_adapter_count == 2:
            expected_vf_used_count_list = [nvf, nvf, nvf, nvf]
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: expected_vf_used_count_list
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        
    def test_create_2pf_64usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        count = 64   
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count
                                  }
        expected_usnic_count_list = []
        for adapter_index in self._cimc_1_adapter_index_list:
            expected_usnic_count_list.extend([count, count])
            self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        expected_usnic_count_list = []
        for adapter_index in self._cimc_2_adapter_index_list:
            expected_usnic_count_list.extend([count, count])
            self.create_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        np = self.calculate_max_number_of_process(Define.CIMC_CORE_PER_NODE, count, DefineMpi.NODE_NUMBER)
        nvf = np/DefineMpi.NODE_NUMBER
        expected_vf_used_count_list = [nvf, nvf]
        if self._cimc_1_adapter_count == 2:
            expected_vf_used_count_list = [nvf, nvf, nvf, nvf]
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: expected_vf_used_count_list
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        expected_vf_used_count_list = [nvf/2, nvf/2]
        if self._cimc_1_adapter_count == 2:
            expected_vf_used_count_list = [nvf/2, nvf/2, nvf/2, nvf/2]
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np/2,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: expected_vf_used_count_list
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
   
    
    def test_create_2pf_diff_usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        adapter_index = self._cimc_1_adapter_index_list[0]   
        usnic_count_dictionary = {
                                "eth0": 65,
                                "eth1": 19
                                  }
        expected_usnic_count_list = [65, 19]
        self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        np = self.calculate_max_number_of_process(Define.CIMC_CORE_PER_NODE, 19, DefineMpi.NODE_NUMBER)
        nvf = np/DefineMpi.NODE_NUMBER
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [nvf, nvf]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
    
    
    def test_create_4pf_16usnic(self):
        self.init_test(inspect.stack()[0][3])
        
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
        
        host_1 = NodeCompute(self._host_ip_1)
        next_available_eth_if_list = host_1.get_next_no_ip_eth_if_name_list(2)
        host_if_ip_dictionary_1 = {
                                 next_available_eth_if_list[0]: "50.35.50." + Util.get_ip_field(DefineMpi.NODE_CIMC_IP_1, 3)+ "/24",
                                 next_available_eth_if_list[1]: "50.35.60." + Util.get_ip_field(DefineMpi.NODE_CIMC_IP_1, 3)+ "/24",
                                 }
        host_if_ip_dictionary_2 = {
                                 next_available_eth_if_list[0]: "50.35.50." + Util.get_ip_field(DefineMpi.NODE_CIMC_IP_2, 3)+ "/24",
                                 next_available_eth_if_list[1]: "50.35.60." + Util.get_ip_field(DefineMpi.NODE_CIMC_IP_2, 3)+ "/24",
                                 }
        
        adapter_index = self._cimc_1_adapter_index_list[0]
        self.create_pf_and_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, host_eth_if_dictionary, usnic_count_dictionary, expected_usnic_count_list, host_if_ip_dictionary_1)
        self.create_pf_and_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, host_eth_if_dictionary, usnic_count_dictionary, expected_usnic_count_list, host_if_ip_dictionary_2)
        
        if self._cimc_1_adapter_count == 2:
            adapter_index = self._cimc_1_adapter_index_list[1]
            usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count,
                                  }
            expected_usnic_count_list = [-1, -1, -1, -1, count, count]
            self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
            self.create_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
            
        np = self.calculate_max_number_of_process(Define.CIMC_CORE_PER_NODE, count, DefineMpi.NODE_NUMBER)
        nvf = np/DefineMpi.NODE_NUMBER
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [nvf, nvf, nvf, nvf]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        ### delete one PF's usnic, then run mpi
        self._logger.info("test run after removing usnic from eth2")
        self._cimc_1.delete_usnic_from_top(adapter_index, "eth2")
        self._cimc_1.power_cycle()
        Util.wait_for_node_to_boot_up(self._host_ip_1)
        
        self._cimc_2.delete_usnic_from_top(adapter_index, "eth2")
        self._cimc_2.power_cycle()
        Util.wait_for_node_to_boot_up(self._host_ip_2)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [nvf, nvf, 0]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        
        ### delete one PF, then run mpi
        self._logger.info("test mpi run after remove eth3")
        self._cimc_1.delete_host_eth_if_from_top(adapter_index, "eth3")
        self._cimc_1.power_cycle()
        Util.wait_for_node_to_boot_up(self._host_ip_1)
        
        self._cimc_2.delete_host_eth_if_from_top(adapter_index, "eth3")
        self._cimc_2.power_cycle()
        Util.wait_for_node_to_boot_up(self._host_ip_2)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [nvf, nvf]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    #suite = unittest.TestLoader().loadTestsFromTestCase(HostDriverTest)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    
    