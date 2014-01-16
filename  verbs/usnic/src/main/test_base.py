'''
Created on Oct 31, 2013

@author: huhe
'''

import time
import os

from main.define import Define, DefineMpi
from lib.util import Util
from lib.logger import MyLogger
from utils.utils import Utils
from lib.cimc import CIMC


class TestBase(object):
    '''
    classdocs
    '''


    def init(self):
        self._logger = MyLogger.getLogger(self.__class__.__name__)    
        self._current_test_log_path = None
        
    
    def check_shell_status(self, positive=True):
        time.sleep(5)
        self._ssh.send("echo status=$?")
        status_str = None#self._logger.debug("\n\n====================== in setUp() ======================")
        if positive:
            status_str = "status=0"
        else:
            status_str = "status=1"
        ret = self._ssh.expect(status_str, 10)
        self.assertEqual(ret, 0)
        
        
    def init_test(self, test_name):
        message = "\n\n====================== " + test_name + " =====================\n\n"
        self._logger.info(message)
        Utils.write_file(Define.PATH_USNIC_LOG_FILE_ALL, message)
        #self._current_test_log_path = Define.PATH_USNIC_LOG + test_name + "_" + Utils.get_current_time_string() + "/"
        #os.makedirs(self._current_test_log_path)
        
    
    def finish_test(self):
        #Utils.move_all_files(Define.PATH_USNIC_LOG, self._current_test_log_path)        
        #Utils.delete_all_files(Define.PATH_USNIC_LOG)
        pass
    

    def run_mpi(self, host, param_dictionary):
        host.run_mpi(param_dictionary)
        shell_status = host.get_shell_status()
        expected_message = DefineMpi.MPI_MESSAGE_DEFAULT
        if DefineMpi.MPI_PARAM_MSG in param_dictionary.keys():
            expected_message = param_dictionary[DefineMpi.MPI_PARAM_MSG]
        if expected_message in DefineMpi.SHELL_STATUS_0_MESSAGE_LIST:
            if host.mpi_run_has_error():
                raise Exception("mpi run has error")
            if host.mpi_run_has_aborted():
                raise Exception("mpi run aborted")
            self.assertEqual(shell_status, 0)
        elif expected_message in DefineMpi.SHELL_STATUS_1_MESSAGE_LIST:
            self.assertEqual(shell_status, 1)
            
        
    def create_pf(self, cimc, adapter_index, host_eth_if_dictionary):
        cimc.create_host_eth_if_from_top(cimc, adapter_index, host_eth_if_dictionary)
        
        
    def create_usnic(self, cimc, adapter_index, usnic_count_dictionary):
        for host_eth_if, usnic_count in sorted(usnic_count_dictionary.iteritems()):
            cimc.create_usnic_from_top(adapter_index, host_eth_if, usnic_count)
            created_usnic_count = cimc.get_usnic_count()
            self.assertEqual(created_usnic_count, usnic_count)
        
    
    def check_host_usnic(self, host, expected_usnic_count_list):
        configured_usnic_count_list = host.get_usnic_configured_count_list()        
        self._logger.info("expected configured usnic count: ")
        self._logger.info(expected_usnic_count_list)
        self._logger.info("actual configured usnic count: ")
        self._logger.info(configured_usnic_count_list)
        for configured_count, expected_count in zip(configured_usnic_count_list, expected_usnic_count_list):
            if expected_count > 0:
                self.assertEqual(configured_count, expected_count)
    
    
    def create_usnic_check_host_usnic(self, cimc, host_ip, adapter_index, usnic_count_dictionary, expected_usnic_count_list):
        self.create_usnic(cimc, adapter_index, usnic_count_dictionary)
        cimc.power_cycle()
        host = Util.wait_for_node_to_boot_up(host_ip)
        self.check_host_usnic(host, expected_usnic_count_list)
        return host
        
        
    def create_pf_and_usnic_check_host_usnic(self, cimc, host_ip, adapter_index, host_eth_if_dictionary, usnic_count_dictionary, expected_usnic_count_list, host_if_ip_dictionary):
        self.create_pf(cimc, adapter_index, host_eth_if_dictionary)
        host = self.create_usnic_check_host_usnic(cimc, host_ip, adapter_index, usnic_count_dictionary, expected_usnic_count_list)
        self.set_host_if_ip(host, host_if_ip_dictionary)
        return host
        
    
    def set_host_if_ip(self, host, host_if_ip_dictionary):
        for int_if, ip_mask in sorted(host_if_ip_dictionary.iteritems()):
            host.set_eth_if_ip(int_if, ip_mask)
        
    
    def create_usnic_for_all_node(self, count):
        usnic_count_dictionary = {
                                "eth0": count,
                                "eth1": count,
                                  }
        for cimc_ip, host_ip in zip(DefineMpi.NODE_CIMC_LIST, DefineMpi.NODE_HOST_LIST):
            cimc = CIMC(cimc_ip)
            for adapter_index in [1, 2]:
                self.create_usnic(cimc, adapter_index, usnic_count_dictionary)
                expected_usnic_count_list = None
                if adapter_index == 1:
                    expected_usnic_count_list = [count, count, -1, -1]
                else:
                    expected_usnic_count_list = [-1, -1, count, count]
                self.check_host_usnic(host_ip, expected_usnic_count_list)
                
                
    def calculate_max_number_of_process(self, number_of_core, number_of_vf, number_of_node, vf_sharing=True):
        if number_of_core > number_of_vf:
            return number_of_vf * number_of_node
        else:
            return number_of_core * number_of_node
        
    
    
    
        
    