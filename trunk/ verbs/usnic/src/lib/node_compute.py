'''
Created on Aug 14, 2013

@author: huhe
'''

import re, threading, time

from main_ucsm.define import Define
from main_ucsm.define_mpi import DefineMpi
from lib.redhat import RedHat
from lib.util import Util


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
        self._ucsm_server_vnic_list = None
        self._usnic_status_dict = {}
        self._usnic_eth_list = {}

    @staticmethod
    def wait_for_node_to_boot_up(node_ip):
        node = None
        probe_max_count = 10
        try_count = 1
        interval = 60
        while try_count <= probe_max_count:
            try:
                node = NodeCompute(node_ip)
                if not node.get_ssh():
                    Util._logger.info("probe times: " + str(try_count))
                    try_count = try_count + 1
                    time.sleep(interval)
                else:
                    return node
            except:
                Util._logger.info("exception is raised in ssh")
                try_count = try_count + 1
                time.sleep(interval)
        raise Exception("Failed to ssh to " + node_ip + " for " + probe_max_count + " times")
            

    def set_ucsm_server_vnic_list(self, vnic_list):
        self._ucsm_server_vnic_list = vnic_list


    def get_ucsm_server_vnic_list(self):
        return self._ucsm_server_vnic_list


    def get_usnic_status_data(self):
        self._ssh.send_expect_prompt("/opt/cisco/usnic/bin/usnic_status")
        output = self._ssh.get_output()
        line_list = output.split("\r\n")
        usnic_index = None
        for line in line_list:
            if line.startswith("usnic_"):
                usnic_index, eth_index, mac_address, vf_configured_count = line.split(", ")
                usnic_index, tmp = usnic_index.split(": ")
                vf_configured_count, tmp = vf_configured_count.split(" ")
                #self._logger.debug("usnic index: " + usnic_index)
                #self._logger.debug("eth: " + eth_index)
                #self._logger.debug("mac address: " + mac_address)
                #self._logger.debug("vf configured count: " + vf_configured_count)
                self._usnic_status_dict[usnic_index] = {"eth": eth_index, "mac": mac_address, "vf configured count": str(vf_configured_count)} 
            else:
                p = re.compile("(?P<VFs>\d+)\sVFs\,\s\d+\sQPs\,\s\d\sCQs")
                m = p.search(line)
                if m:
                    vfs = m.groups("VFs")[0]
                    #self._logger.debug("vf used count: " + vfs)
                    self._usnic_status_dict[usnic_index]["vf used count"] = vfs
        self._logger.debug(self._usnic_status_dict)


    def get_ifconfig_data(self):
        self._ssh.send_expect_prompt("ifconfig")
        output = self._ssh.get_output()
        line_list = output.split("\r\n")
        p_eth = re.compile("(?P<eth>^eth[0-9\.]+)")
        p_ip  = re.compile("(?<=inet addr:)((?:\d{1,3}\.){3}\d{1,3})")
        p_mtu = re.compile("(?<=MTU:)(\d+)")
        eth_index = None
        for line in line_list:
            m = p_eth.search(line)
            if m:
                eth_index = m.groups("eth")[0]
                self._usnic_eth_list[eth_index] = {}
            elif eth_index:
                m = p_ip.search(line)
                if m:
                    ip = m.groups("ip")[0]
                    self._usnic_eth_list[eth_index]["ip"] = ip
                m = p_mtu.search(line)
                if m:
                    mtu = m.groups("mtu")[0]
                    self._usnic_eth_list[eth_index]["mtu"] = mtu
        print self._usnic_eth_list
        

    def start_pingpong_server(self, usnic):
        self._ssh.send_expect_prompt("ibv_ud_pingpong -g 0 -s 100 -d " + usnic)
        return Util.check_shell_status(self._ssh)
    

    def start_pingpong_client(self, usnic, ip_address):
        self._ssh.send_expect_prompt("ibv_ud_pingpong -g 0 -s 100 -d " + usnic + " " + ip_address)
        return Util.check_shell_status(self._ssh)
    

    def usnic_verbs_check(self):
        self._ssh.send_expect_prompt("usnic_verbs_check")
        
        
    def usnic_status(self):
        self._ssh.send_expect_prompt("usnic_status")
        

    def get_usnic_eth_if_ip_list(self):
        usnic_eth_if_ip_list = []
        if not self._eth_if_list:
            usnic_eth_if_list = self._ssh.send_match_list("usnic_status", "(?<=\, )(?:eth\d)")
            for usnic_eth_if in usnic_eth_if_list:
                usnic_eth_if_ip_list_tmp = self._ssh.send_match_list("ifconfig " + usnic_eth_if, "(?<=inet addr:)((?:\d{1,3}\.){3}\d{1,3})")
                if len(usnic_eth_if_ip_list_tmp) == 1:
                    usnic_eth_if_ip_list.append(usnic_eth_if_ip_list_tmp[0])
        return usnic_eth_if_ip_list
    
        
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
        
        