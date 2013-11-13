'''
Created on Aug 14, 2013

@author: huhe
'''

import re, threading, time

from main.define import Define, DefineMpi
from lib.redhat import RedHat

class NodeCompute(RedHat):
    '''
    classdocs
    '''


    def __init__(self, hostname, username=Define.NODE_DEFAULT_USERNAME, password=Define.NODE_DEFAULT_PASSWORD):
        '''
        Constructor
        '''
        RedHat.__init__(self, hostname, username, password)        
        self._current_output = None
        self._vf_used_count_equal_dictionary = {}

        
    def get_usnic_configured_count_list(self):
        usnic_count_list = []
        ret_list = self._ssh.send_match_list("/opt/cisco/usnic/bin/usnic_status", "(?:\d+)\sVFs")
        ret_list = [int(x.replace(" VFs", "")) for x in ret_list]
        for index, element in enumerate(ret_list):
            if index % 2 == 0:
                usnic_count_list.append(element)
        return usnic_count_list
    
    def get_usnic_used_count_list(self):
        usnic_count_list = []
        ret_list = self._ssh.send_match_list("/opt/cisco/usnic/bin/usnic_status", "(?:\d+)\sVFs")
        ret_list = [int(x.replace(" VFs", "")) for x in ret_list]
        for index, element in enumerate(ret_list):
            if index % 2 == 1:
                usnic_count_list.append(element)
        return usnic_count_list
    
    
    def check_used_vf_count(self, host_ip_list, expected_vf_used_count_list):
        for host_ip in host_ip_list:
            self._logger.info("host: " + host_ip)
            host = NodeCompute(host_ip)
            actual_vf_used_count_list = host.get_usnic_used_count_list()
            self._logger.info("expected vf used count list: ")
            self._logger.info(expected_vf_used_count_list)
            self._logger.info("actual vf used count list: ")
            self._logger.info(actual_vf_used_count_list)
            
            vf_used_count_equal = True
            for configured_count, expected_count in zip(actual_vf_used_count_list, expected_vf_used_count_list):
                if expected_count >= 0:
                    if configured_count != expected_count:
                        vf_used_count_equal = False
                        break
                    
            if vf_used_count_equal:
                self._logger.info("vf used counts equal")
                self._vf_used_count_equal_dictionary[host_ip] = True
            else:
                self._logger.error("vf used counts not equal")
                self._vf_used_count_equal_dictionary[host_ip] = False
                        
            host.exit()
            
            
    
    def run_mpi(self, param_dictionary):
        
        cmd = DefineMpi.MPI_CMD_DEFAULT
        np  = DefineMpi.MPI_NP_DEFAULT
        mca = DefineMpi.MPI_MCA_DEFAULT 
        msg = DefineMpi.MPI_MESSAGE_DEFAULT
        host_ip_list = DefineMpi.NODE_HOST_LIST_DEFAULT
        
        vf_used_count_list = None
        check_used_vf_count_flag = False
        
        key_list = param_dictionary.keys()
        if DefineMpi.MPI_PARAM_HOST in key_list:
            host_ip_list = param_dictionary[DefineMpi.MPI_PARAM_HOST]
        if DefineMpi.MPI_PARAM_NP in key_list:
            np = param_dictionary[DefineMpi.MPI_PARAM_NP]
        if DefineMpi.MPI_PARAM_MCA in key_list:
            mca = param_dictionary[DefineMpi.MPI_PARAM_MCA]
        if DefineMpi.MPI_PARAM_CMD in key_list:
            cmd = param_dictionary[DefineMpi.MPI_PARAM_CMD]
        if DefineMpi.MPI_PARAM_MSG in key_list:
            msg = param_dictionary[DefineMpi.MPI_PARAM_MSG]
        if DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST in key_list:
            vf_used_count_list = param_dictionary[DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST]
            check_used_vf_count_flag = True
        
        host_str = " ".join([DefineMpi.MPI_PARAM_HOST, ",".join(host_ip_list)])
        np_str   = " ".join([DefineMpi.MPI_PARAM_NP, str(np)])
        mca_str  = " ".join([DefineMpi.MPI_PARAM_MCA, mca])
        cmd_str  = " ".join(["mpirun", host_str, np_str, mca_str, DefineMpi.MPI_PATH, cmd])
        
        timeout = DefineMpi.MPI_CMD_TIMEOUT_ALL
        if cmd == DefineMpi.MPI_CMD_PINGPONG:
            timeout = DefineMpi.MPI_CMD_TIMEOUT_PINGPONG
        elif cmd == DefineMpi.MPI_CMD_ALLTOALL:
            timeout = DefineMpi.MPI_CMD_TIMEOUT_ALLTOALL
        
        self._logger.info(cmd_str)
        self._logger.debug("timeout: " + str(timeout))
        self._ssh.send(cmd_str)
        
        if check_used_vf_count_flag and cmd != DefineMpi.MPI_CMD_PINGPONG:
            time.sleep(10)
            find_used_vf_count_thread = threading.Thread(target=self.check_used_vf_count, args=(host_ip_list, vf_used_count_list))
            find_used_vf_count_thread.daemon = True
            find_used_vf_count_thread.start()
        
        prompt_pattern = self._username + "@" + self._hostname + ".+$"
        self._ssh.expect(prompt_pattern, timeout)
        self._current_output = self._ssh.get_output()
        
        if re.search(msg, self._current_output, re.IGNORECASE):
            self._logger.info("found message: " + msg)
            if msg in DefineMpi.SHELL_STATUS_0_MESSAGE_LIST:
                if check_used_vf_count_flag:
                    for host_ip, result in self._vf_used_count_equal_dictionary.iteritems():
                        self._logger.info(host_ip)
                        self._logger.info(result)
                        if not result:
                            return False
                    return True
            else:
                return True
        else:
            self._logger.error("could not find message: " + msg)
            if self.mpi_run_has_error():
                self._logger.error("found error message")
            if self.mpi_run_has_aborted():
                self._logger.error("found abort message")
            if self.mpi_run_not_enough_core():
                self._logger.error("found not enough core message")
            if self.mpi_run_not_enough_usnic():
                self._logger.error("found not enough usnic message")
            return False
    
    
    def mpi_run_has_error(self):
        if re.search(DefineMpi.MPI_MESSAGE_ERROR, self._current_output, re.IGNORECASE):
            return True
        else:
            return False
        
        
    def mpi_run_has_aborted(self):
        if re.search(DefineMpi.MPI_MESSAGE_ABORT, self._current_output, re.IGNORECASE):
            return True
        else:
            return False
        
    def mpi_run_not_enough_usnic(self):
        if re.search(DefineMpi.MPI_MESSAGE_NOT_ENOUGH_VNIC, self._current_output, re.IGNORECASE):
            return True
        else:
            return False
        
        
    def mpi_run_not_enough_core(self):
        if re.search(DefineMpi.MPI_MESSAGE_NOT_ENOUGH_CORE, self._current_output, re.IGNORECASE):
            return True
        else:
            return False
        
        