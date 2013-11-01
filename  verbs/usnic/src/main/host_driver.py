'''
Created on Oct 31, 2013

@author: huhe
'''
import unittest
import inspect

from main.define import Define
from main import define
from lib.node_compute import NodeCompute
from main.test_base import TestBase
from utils.utils import Utils


class HostDriverTest(unittest.TestCase, TestBase):

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
        
        self._node1 = NodeCompute(Define.HOST_DRIVER_1, Define.NODE_DEFAULT_USERNAME, Define.NODE_DEFAULT_PASSWORD)        
        TestBase.init(self, self._node1.get_ssh())

    def tearDown(self):
        self._ssh.exit()
        Utils.append_file(Define.PATH_USNIC_LOG_FILE_ALL, Define.PATH_USNIC_LOG_FILE)

    
    def test_run_mpi_pingpong(self):
        self.init_test(inspect.stack()[0][3])
        test_type = True
        self.run_mpi(self.__mpi_pingpong, 30)
        self.check_status(test_type)
    
        
    def test_unload_enic_failure(self):
        self.init_test(inspect.stack()[0][3])
        test_type = False
        self.send("modprobe -r enic")
        ret = self.expect("FATAL: Module enic is in use.")
        self.assertEqual(ret, 0)
        self.check_status(test_type)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    #suite = unittest.TestLoader().loadTestsFromTestCase(HostDriverTest)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    
    