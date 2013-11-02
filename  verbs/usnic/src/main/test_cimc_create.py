'''
Created on Oct 31, 2013

@author: huhe
'''
import unittest
import inspect

from main.define import Define
from main import define
from lib.cimc import CIMC
from main.test_base import TestBase
from utils.utils import Utils


class TestCimcCreate(unittest.TestCase, TestBase):

    @classmethod
    def setUpClass(cls):
        mpi_host = " ".join([Define.MPI_HOST, Define.HOST_DRIVER_1+","+Define.HOST_DRIVER_2])
        mpi_np   = " ".join([Define.MPI_NP, str(32)])
        mpi_cmd = " ".join(["mpirun", mpi_host, mpi_np, Define.MPI_MCA, Define.MPI_PATH, Define.MPI_CMD_PINGPOND])
        cls.__mpi_pingpong = mpi_cmd
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        define.PEXPECT_OUTPUT_STDOUT = False
        
        self._cimc_1 = CIMC(Define.CIMC_IP_1)        
        TestBase.init(self, self._cimc_1.get_ssh())

    def tearDown(self):
        self._cimc_1._ssh.exit()
        Utils.append_file(Define.PATH_USNIC_LOG_FILE_ALL, Define.PATH_USNIC_LOG_FILE)

    @unittest.skip
    def test_run_mpi_pingpong(self):
        self.init_test(inspect.stack()[0][3])
        test_type = True
        self.run_mpi(self.__mpi_pingpong, 30)
        self.check_status(test_type)
    
    @unittest.skip    
    def test_create_1pf_usnic_default_host_eth_if(self):
        self.init_test(inspect.stack()[0][3])
        
        ''' remove usnic from eth1 '''
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
    
    @unittest.skip  
    def test_create_1pf_usnic_max_default_host_eth_if_negative(self):
        self.init_test(inspect.stack()[0][3])
        test_type = False
        
        ''' remove usnic from eth1 '''
        adapter_index = 1        
        host_eth_if = "eth1"
        self._cimc_1.delete_usnic_from_top(adapter_index, host_eth_if)
        
        host_eth_if = "eth0"
        count = Define.CIMC_MAX_USNIC_PER_ADAPTER + 1
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
    
    
    