'''
Created on Oct 31, 2013

@author: huhe
'''
import unittest
import inspect

from main.define import Define, DefineMpi
from main import define
from main.test_base import TestBase
from utils.utils import Utils


class TestMpiRun(unittest.TestCase, TestBase):

    @classmethod
    def setUpClass(cls):
        pass
    
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    
    def setUp(self):
        define.PEXPECT_OUTPUT_STDOUT = False
        self._host = DefineMpi.NODE_HOST_IP_1
        TestBase.init(self, None)
        
        '''
        bcnode01-02: cores = 40
        usnic = 32
        self.create_usnic_for_all_node(32)
        '''
        
    def tearDown(self):
        Utils.append_file(Define.PATH_USNIC_LOG_FILE_ALL, Define.PATH_USNIC_LOG_FILE)

    
    def test_include_1usnic(self):
        self.init_test(inspect.stack()[0][3])        
        
        for i in range(0, 4):
            mpi_cmd = self.construct_mpi_cmd(DefineMpi.MPI_PINGPONG, 32, DefineMpi.NODE_HOST_LIST, DefineMpi.MPI_MCA_INCLUDE_USNIC_PREFIX+str(i))
            self.run_mpi(self._host, mpi_cmd, DefineMpi.MPI_MESSAGE_FINISH)
            
        
    def test_include_2usnic(self):
        self.init_test(inspect.stack()[0][3])        
        
        mpi_cmd = self.construct_mpi_cmd(DefineMpi.MPI_PINGPONG, 32, DefineMpi.NODE_HOST_LIST, "btl_usnic_include usnic_0,usnic_1")
        self.run_mpi(self._host, mpi_cmd, DefineMpi.MPI_MESSAGE_FINISH)
    
            
    def test_include_1eth(self):
        self.init_test(inspect.stack()[0][3])        
        
        for i in range(4, 8):
            mpi_cmd = self.construct_mpi_cmd(DefineMpi.MPI_PINGPONG, 32, DefineMpi.NODE_HOST_LIST, DefineMpi.MPI_MCA_INCLUDE_ETH_PREFIX+str(i))
            self.run_mpi(self._host, mpi_cmd, DefineMpi.MPI_MESSAGE_FINISH)
        
        
    def test_include_2eth(self):
        self.init_test(inspect.stack()[0][3])        
        
        mpi_cmd = self.construct_mpi_cmd(DefineMpi.MPI_PINGPONG, 32, DefineMpi.NODE_HOST_LIST, "btl_usnic_include eth8,eth6")
        self.run_mpi(self._host, mpi_cmd, DefineMpi.MPI_MESSAGE_FINISH)
    
                

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    #suite = unittest.TestLoader().loadTestsFromTestCase(HostDriverTest)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    
    