'''
Created on Oct 31, 2013

@author: huhe
'''
import unittest
import inspect

from main.define import Define, DefineMpi
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
    
        TestCimcCreate.__cimc_1_adapter_index_list = TestCimcCreate.__cimc_1.get_adapter_index_list_from_top()
        TestCimcCreate.__cimc_2_adapter_index_list = TestCimcCreate.__cimc_2.get_adapter_index_list_from_top()
        
    
    @classmethod
    def tearDownClass(cls):
        TestCimcCreate.__cimc_1._ssh.exit()
        TestCimcCreate.__cimc_2._ssh.exit()
    
    
    def setUp(self):
        TestBase.init(self)
        #self._logger.debug("\n\n====================== in setUp() ======================")
        self._host_ip_1 = TestCimcCreate.__host_ip_1
        self._host_ip_2 = TestCimcCreate.__host_ip_2
        
        self._cimc_1 = TestCimcCreate.__cimc_1
        self._cimc_2 = TestCimcCreate.__cimc_2
        
        self._cimc_1.show_cimc_detail()
        self._cimc_2.show_cimc_detail()
        
        self._cimc_1_adapter_index_list = TestCimcCreate.__cimc_1_adapter_index_list
        self._cimc_2_adapter_index_list = TestCimcCreate.__cimc_2_adapter_index_list
        
        self._cimc_1_adapter_count = len(self._cimc_1_adapter_index_list)
        self._cimc_2_adapter_count = len(self._cimc_2_adapter_index_list)
        
        for adapter_index in self._cimc_1_adapter_index_list:
            self._cimc_1.delete_all_host_eth_if_from_top(adapter_index)
        for adapter_index in self._cimc_2_adapter_index_list:
            self._cimc_2.delete_all_host_eth_if_from_top(adapter_index)
        
        
    def tearDown(self):
        self.finish_test()

    
    def test_usnic_mtu1500_cos0(self):
        self.init_test(inspect.stack()[0][3])
        
        usnic_count = 16
        mtu = 1500
        cos = 0
        self.mtu_cos_test(usnic_count, mtu, cos)
    
        
    def test_usnic_mtu1500_cos5(self):
        self.init_test(inspect.stack()[0][3])
        
        usnic_count = 16
        mtu = 1500
        cos = 5
        self.mtu_cos_test(usnic_count, mtu, cos)
        
    
    def test_usnic_mtu9000_cos0(self):
        self.init_test(inspect.stack()[0][3])
        
        usnic_count = 16
        mtu = 9000
        cos = 0
        self.mtu_cos_test(usnic_count, mtu, cos)
    
        
    def test_usnic_mtu9000_cos5(self):
        self.init_test(inspect.stack()[0][3])
        
        usnic_count = 16
        mtu = 9000
        cos = 5
        self.mtu_cos_test(usnic_count, mtu, cos)
        
        
    def mtu_cos_test(self, usnic_count, mtu, cos):
        
        self.create_usnic_mtu_cos(self._cimc_1, self._host_ip_1, self._cimc_1_adapter_index_list, usnic_count, mtu, cos)
        self.create_usnic_mtu_cos(self._cimc_2, self._host_ip_2, self._cimc_2_adapter_index_list, usnic_count, mtu, cos)
        
        self.prepare_and_run_mpi(usnic_count)
        
        
    def prepare_and_run_mpi(self, usnic_count):
        np = self.calculate_max_number_of_process(Define.CIMC_CORE_PER_NODE, usnic_count, DefineMpi.NODE_NUMBER)
        nvf = np/DefineMpi.NODE_NUMBER
        expected_vf_used_count_list = [nvf, nvf]
        if self._cimc_1_adapter_count == 2:
            expected_vf_used_count_list = [nvf, nvf, nvf, nvf]
        param_dictionary = {
                            DefineMpi.MPI_PARAM_CMD: DefineMpi.MPI_CMD_ALLTOALL,
                            DefineMpi.MPI_PARAM_NP: np,
                            DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST: expected_vf_used_count_list
                            }
        host_1 = NodeCompute(self._host_ip_1)
        self.run_mpi(host_1, param_dictionary)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    #suite = unittest.TestLoader().loadTestsFromTestCase(HostDriverTest)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    
    