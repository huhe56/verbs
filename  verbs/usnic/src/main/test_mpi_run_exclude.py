'''
Created on Oct 31, 2013

@author: huhe
'''
import unittest
import inspect

from main.define import DefineMpi, Define
from main import define
from lib.cimc import CIMC
from lib.node_compute import NodeCompute
from main.test_base import TestBase


class TestMpiRunExclude(unittest.TestCase, TestBase):
    ''' need 4 usnic interface server '''
    
    @classmethod
    def setUpClass(cls):
        define.PEXPECT_OUTPUT_STDOUT = False
        TestMpiRunExclude.__host_ip_1 = DefineMpi.NODE_HOST_IP_1
        TestMpiRunExclude.__host_ip_2 = DefineMpi.NODE_HOST_IP_2
        TestMpiRunExclude.__cimc_1 = CIMC(DefineMpi.NODE_CIMC_IP_1)  
        TestMpiRunExclude.__cimc_2 = CIMC(DefineMpi.NODE_CIMC_IP_2)
    
        TestMpiRunExclude.__cimc_1_adapter_index_list = TestMpiRunExclude.__cimc_1.get_adapter_index_list_from_top()
        TestMpiRunExclude.__cimc_2_adapter_index_list = TestMpiRunExclude.__cimc_2.get_adapter_index_list_from_top()
        
    
    @classmethod
    def tearDownClass(cls):
        TestMpiRunExclude.__cimc_1._ssh.exit()
        TestMpiRunExclude.__cimc_2._ssh.exit()
    
    
    def setUp(self):
        TestBase.init(self)
        
        self._host_ip_1 = TestMpiRunExclude.__host_ip_1
        self._host_ip_2 = TestMpiRunExclude.__host_ip_2
        
        self._cimc_1 = TestMpiRunExclude.__cimc_1
        self._cimc_2 = TestMpiRunExclude.__cimc_2
        
        self._cimc_1.show_cimc_detail()
        self._cimc_2.show_cimc_detail()
        
        self._cimc_1_adapter_index_list = TestMpiRunExclude.__cimc_1_adapter_index_list
        self._cimc_2_adapter_index_list = TestMpiRunExclude.__cimc_2_adapter_index_list
        
        self._cimc_1_adapter_count = len(self._cimc_1_adapter_index_list)
        self._cimc_2_adapter_count = len(self._cimc_2_adapter_index_list)
        
        for adapter_index in self._cimc_1_adapter_index_list:
            self._cimc_1.delete_all_host_eth_if_from_top(adapter_index)
        for adapter_index in self._cimc_2_adapter_index_list:
            self._cimc_2.delete_all_host_eth_if_from_top(adapter_index)
        
                
    def tearDown(self):
        self.finish_test()
    
    
    # first test to run to setup environment
    @unittest.skip("")
    def test_0_create_2pf_16usnic_run_mpi(self):
        self.init_test(inspect.stack()[0][3])
        
        count = 16    
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count
                                  }
        
        expected_usnic_count_list = []
        for adapter_index in self._cimc_1_adapter_index_list:
            expected_usnic_count_list.append(count)
            expected_usnic_count_list.append(count)
            self.create_usnic_check_host_usnic(self._cimc_1, self._host_ip_1, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        expected_usnic_count_list = []
        for adapter_index in self._cimc_2_adapter_index_list:
            expected_usnic_count_list.append(count)
            expected_usnic_count_list.append(count)
            self.create_usnic_check_host_usnic(self._cimc_2, self._host_ip_2, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        
        np = self.calculate_max_number_of_process(Define.CIMC_CORE_PER_NODE, count, DefineMpi.NODE_NUMBER)
        nvf = np/DefineMpi.NODE_NUMBER
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [nvf, nvf]
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        
    def test_exclude_if_usnic(self):
        self.init_test(inspect.stack()[0][3])
        
        count = 16
        np = self.calculate_max_number_of_process(Define.CIMC_CORE_PER_NODE, count, DefineMpi.NODE_NUMBER)
        nvf = np/DefineMpi.NODE_NUMBER
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_MCA: "btl_usnic_if_exclude usnic_0",
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [0, nvf, nvf, nvf]
                             
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_MCA: "btl_usnic_if_exclude usnic_3,usnic_1",
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [nvf, 0, nvf, 0]
                             
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_MCA: "btl_usnic_if_exclude usnic_0,usnic_2,usnic_1",
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [0, 0, 0, nvf]
                             
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
    
    @unittest.skip("future support feature")
    def test_exclude_if_eth(self):
        self.init_test(inspect.stack()[0][3])
        
        count = 16
        np = self.calculate_max_number_of_process(Define.CIMC_CORE_PER_NODE, count, DefineMpi.NODE_NUMBER)
        nvf = np/DefineMpi.NODE_NUMBER
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_MCA: "btl_usnic_if_exclude eth4",
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [nvf, 0, 0, 0]
                             
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_MCA: "btl_usnic_if_exclude eth5,eth7",
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [nvf, 0, nvf, 0]
                             
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_MCA: "btl_usnic_if_exclude eth4,eth6,eth7",
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [0, nvf, 0, 0]
                             
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)


    def test_exclude_if_network(self):
        self.init_test(inspect.stack()[0][3])
        
        count = 16
        np = self.calculate_max_number_of_process(Define.CIMC_CORE_PER_NODE, count, DefineMpi.NODE_NUMBER)
        nvf = np/DefineMpi.NODE_NUMBER
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_MCA: "btl_usnic_if_exclude 50.35.10.0/24",
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [0, nvf, nvf, nvf]
                             
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_MCA: "btl_usnic_if_exclude 50.35.20.0/24,50.35.40.0/24",
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [nvf, 0, nvf, 0]
                             
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        
        param_dictionary = {
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_MCA: "btl_usnic_if_exclude 50.35.30.0/24,50.35.20.0/24,50.35.40.0/24",
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: [nvf, 0, 0, 0]
                             
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    #suite = unittest.TestLoader().loadTestsFromTestCase(HostDriverTest)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    
    