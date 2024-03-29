'''
Created on Aug 14, 2013

@author: huhe
'''

import re, threading, time, socket

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
        self._vf_used_count_equal_dict = {}
        self._ucsm_server_vnic_dict = None
        self._usnic_status_dict = {}
        self._usnic_eth_list = {}
        self._total_cpu_core_count = None
        self._np = None
        self._min_total_cpu_core_count = None
        self._vf_sharing = True

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
                    node.get_ssh().send_expect_prompt("uptime")
                    return node
            except:
                Util._logger.info("exception is raised in ssh")
                try_count = try_count + 1
                time.sleep(interval)
        raise Exception("Failed to ssh to " + node_ip + " for " + probe_max_count + " times")
            

    def set_vf_sharing(self, vf_sharing):
        self._vf_sharing = vf_sharing
        self._ssh.send("su -")
        self._ssh.expect("assword: ")
        self._ssh.send_expect_prompt(Define.NODE_DEFAULT_PASSWORD)
        cmd = None
        if self._vf_sharing:
            self._logger.info(self._hostname + ", setting vf sharing")
            cmd = "echo 1 > /sys/module/usnic_verbs/parameters/usnic_ib_share_vf"
        else:
            self._logger.info(self._hostname + ", setting vf not sharing")
            cmd = "echo 0 > /sys/module/usnic_verbs/parameters/usnic_ib_share_vf"
        self._ssh.send_expect_prompt(cmd)
        self._ssh.send_expect_prompt("cat /sys/module/usnic_verbs/parameters/usnic_ib_share_vf")
        self._ssh.send_expect_prompt("exit")
        

    def set_min_total_cpu_core_count(self, count):
        self._min_total_cpu_core_count = count
        
        
    def get_min_total_cpu_core_count(self):
        return self._min_total_cpu_core_count
        

    def set_np(self, np):
        self._np = np
        
        
    def get_np(self):
        return self._np
    

    def set_total_cpu_core_count(self, count):
        self._total_cpu_core_count = count
        
    
    def get_total_cpu_core_count(self):
        return self._total_cpu_core_count
    
        
    def set_ucsm_server_vnic_dict(self, vnic_dict):
        self._ucsm_server_vnic_dict = vnic_dict


    def get_ucsm_server_vnic_dict(self):
        return self._ucsm_server_vnic_dict


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
                self._usnic_status_dict[usnic_index] = {"eth": eth_index, "mac": mac_address.upper(), "vf configured count": int(vf_configured_count)} 
            else:
                p = re.compile("(?P<VFs>\d+)\sVFs\,\s\d+\sQPs\,\s\d+\sCQs")
                m = p.search(line)
                if m:
                    vfs = m.groups("VFs")[0]
                    self._usnic_status_dict[usnic_index]["vf used count"] = int(vfs)
        self._logger.debug(self._usnic_status_dict)


    def get_ifconfig_data(self):
        self._ssh.send_expect_prompt("ifconfig -a")
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
                    self._usnic_eth_list[eth_index]["mtu"] = int(mtu)
                    eth_index = None
        self._logger.debug(self._usnic_eth_list)
        
    
    def set_host_ip_mtu(self):
        self._logger.info(self._hostname + " setting host mtu if any ...")
        self.get_usnic_status_data()
        self.get_ifconfig_data()
        for vnic_name, vnic_data in self._ucsm_server_vnic_dict.items():
            vnic_mac = vnic_data.get_mac_address()
            vnic_mtu = vnic_data.get_mtu()
            vnic_vlan = vnic_data.get_vlan()
            for usnic_index, usnic_status_data in self._usnic_status_dict.items():
                usnic_mac = usnic_status_data["mac"]
                usnic_eth = usnic_status_data["eth"]
                if vnic_mac == usnic_mac:
                    if vnic_vlan >= 200:
                        ''' handle 32 PFs case '''
                        item_list = self._usnic_eth_list["eth0"]["ip"].split(".")
                        eth_ip = ".".join(["50", item_list[2], str(vnic_vlan), item_list[3]])
                        #print usnic_eth + ", " + eth_ip
                        ip_mask = eth_ip + "/24"
                        self.set_eth_if_ip(usnic_eth, ip_mask)
                    eth_mtu = self._usnic_eth_list[usnic_eth]["mtu"]
                    if vnic_mtu != eth_mtu:
                        self._logger.info(self._hostname + ", " + usnic_eth + ", mtu set from " + str(eth_mtu) + " to " + str(vnic_mtu))
                        self.set_mtu(usnic_eth, vnic_mtu)
                        break
        self.show_ifconfig()
    
        
    def check_usnic_configured_vf(self):
        self._logger.info(self._hostname + ": checking host configured vf count ...")
        self.get_usnic_status_data()
        for vnic_name, vnic_data in self._ucsm_server_vnic_dict.items():
            if vnic_data.get_usnic_count() > 0:
                match = False
                vnic_mac = vnic_data.get_mac_address()
                vnic_usnic_count = vnic_data.get_usnic_count()
                vnic_str = None
                eth_str = None
                for usnic_index, usnic_status_data in self._usnic_status_dict.items():
                    usnic_mac = usnic_status_data["mac"]
                    usnic_vf_configured_count = usnic_status_data["vf configured count"]
                    vnic_str = "vnic " + vnic_name + " mac [" + vnic_mac + "] and usnic count [" + str(vnic_usnic_count) +"]"
                    eth_str  = "eth "  + usnic_index + " mac [" + usnic_mac + "] and usnic count [" + str(usnic_vf_configured_count) + "]"                        
                    if vnic_mac == usnic_mac and vnic_usnic_count == usnic_vf_configured_count:
                        self._logger.info("Passed: vnic and eth mac and usnic count are the same")
                        self._logger.info("Passed: " + vnic_str)
                        self._logger.info("Passed: " + eth_str)
                        match = True
                        break
                if not match:
                    self._logger.error("Failed: vnic and eth mac and usnic count are not the same")
                    self._logger.error("Failed: " + vnic_str)
                    self._logger.error("Failed: " + eth_str)
                    raise Exception("Failed to match vnic and eth mac and usnic count")
                    
        

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
    
    
    def check_usnic_used_vf(self):
        self._logger.info(self._hostname + " checking host used vf count ...")
        self.get_usnic_status_data()
        for vnic_name, vnic_data in self._ucsm_server_vnic_dict.items():
            if vnic_data.get_usnic_count() > 0:
                match_mac = False
                vnic_mac = vnic_data.get_mac_address()
                vnic_usnic_count = vnic_data.get_usnic_count()
                expected_vf_used_count = vnic_data.get_expect_used_usnic_count()
                vnic_str = None
                eth_str = None
                for usnic_index, usnic_status_data in self._usnic_status_dict.items():
                    usnic_mac = usnic_status_data["mac"]
                    usnic_vf_configured_count = usnic_status_data["vf configured count"]
                    usnic_vf_used_count = usnic_status_data["vf used count"]
                    
                    if expected_vf_used_count == None:
                        expected_vf_used_count = 0 if vnic_usnic_count < self._np else self._np
                    
                    vnic_str = "vnic " + vnic_name + " mac [" + vnic_mac + "], usnic configured count [" + str(vnic_usnic_count) +"], expect used count [" + str(expected_vf_used_count) + "]"
                    eth_str  = "eth "  + usnic_index + " mac [" + usnic_mac + "], usnic configured count [" + str(usnic_vf_configured_count) + "], actual used count [" + str(usnic_vf_used_count) + "]"     
                                       
                    if vnic_mac == usnic_mac:
                        match_mac = True
                        if expected_vf_used_count == usnic_vf_used_count and vnic_usnic_count == usnic_vf_configured_count:
                            self._logger.info("Passed: vnic and eth's mac and usnic count are the same")
                            self._logger.info("Passed: " + vnic_str)
                            self._logger.info("Passed: " + eth_str)
                            break
                        else:
                            self._logger.info("Failed: vnic and eth's mac and usnic count are not the same")
                            self._logger.info("Failed: " + vnic_str)
                            self._logger.info("Failed: " + eth_str)
                            return False
                if not match_mac:
                    self._logger.error("Failed: can not find matched vnic mac address " + vnic_mac + " in host usnic interface")
                    return False
            
        return True
        
    
    def check_all_hosts_used_vf(self, host_list):
        for host in host_list:
            ret = host.check_usnic_used_vf()        
            if ret:
                self._logger.info("#"*10 + " " + host.get_host_name() + " vf used counts equal")
                self._vf_used_count_equal_dict[host.get_host_name()] = True
            else:
                self._logger.error("*"*10 + " " + host.get_host_name() + " vf used counts not equal")
                self._vf_used_count_equal_dict[host.get_host_name()] = False
            host.exit()
            
    
    def run_mpi(self, param_dictionary, test_case_type):
                
        cmd = None
        np_str = None
        host_list = None
        msg_list = None
        mca = DefineMpi.MPI_MCA_DEFAULT 
        bind_to_none = False
        
        key_list = param_dictionary.keys()
        if DefineMpi.MPI_PARAM_HOST_LIST in key_list:
            host_list = param_dictionary[DefineMpi.MPI_PARAM_HOST_LIST]
        if DefineMpi.MPI_PARAM_NP in key_list:
            np_str = param_dictionary[DefineMpi.MPI_PARAM_NP]
        if DefineMpi.MPI_PARAM_MCA in key_list:
            mca = param_dictionary[DefineMpi.MPI_PARAM_MCA]
        if DefineMpi.MPI_PARAM_CMD in key_list:
            cmd = param_dictionary[DefineMpi.MPI_PARAM_CMD]
        if DefineMpi.MPI_PARAM_MSG in key_list:
            msg_list = param_dictionary[DefineMpi.MPI_PARAM_MSG]
        if DefineMpi.MPI_PARAM_BIND_TO_NONE in key_list:
            bind_to_none = param_dictionary[DefineMpi.MPI_PARAM_BIND_TO_NONE]
            
        np = None
        total_np = None
        if not np_str:
            np = self._min_total_cpu_core_count
            total_np = self._min_total_cpu_core_count * len(host_list)
        else:
            np = int(np_str)
            total_np = int(np_str) * len(host_list)
            
        timeout = DefineMpi.MPI_CMD_TIMEOUT_ALL
        if cmd == DefineMpi.MPI_CMD_PINGPONG:
            timeout = DefineMpi.MPI_CMD_TIMEOUT_PINGPONG
        elif cmd == DefineMpi.MPI_CMD_ALLTOALL:
            timeout = DefineMpi.MPI_CMD_TIMEOUT_ALLTOALL
        elif cmd == DefineMpi.MPI_CMD_ALL:
            timeout = DefineMpi.MPI_CMD_TIMEOUT_ALL
            cmd = ""    
        
        host_name_list = [host.get_host_name() for host in host_list]
        host_str = " ".join([DefineMpi.MPI_PARAM_HOST, ",".join(host_name_list)])
        bind_to_none_str = "" if not bind_to_none else DefineMpi.MPI_BIND_TO_NONE
        np_str   = " ".join([DefineMpi.MPI_PARAM_NP, str(total_np)])
        mca_str  = " ".join([DefineMpi.MPI_PARAM_MCA, mca]) if mca else ""
        cmd_str  = " ".join(["mpirun", host_str, bind_to_none_str, np_str, mca_str, DefineMpi.MPI_PATH, cmd])
        
        self._logger.info(cmd_str)
        self._logger.debug("timeout: " + str(timeout))
        self._ssh.send(cmd_str)
        
        if cmd != DefineMpi.MPI_CMD_PINGPONG:
            time.sleep(10)
            new_host_list = []
            for host in host_list:
                new_host = NodeCompute(host.get_host_name())
                new_host.set_ucsm_server_vnic_dict(host.get_ucsm_server_vnic_dict())
                new_host.set_total_cpu_core_count(host.get_total_cpu_core_count())
                new_host.set_np(np)
                new_host_list.append(new_host)
            find_used_vf_count_thread = threading.Thread(target=self.check_all_hosts_used_vf, args=[new_host_list])
            find_used_vf_count_thread.daemon = True
            find_used_vf_count_thread.start()
            find_used_vf_count_thread.join()
        
        prompt_pattern = self._username + "@" + self._hostname + ".+$"
        self._ssh.expect(prompt_pattern, timeout)
        self._current_output = self._ssh.get_output()
        
        test_case_passed = True
        found_all_messages = True
        for msg_index in msg_list:
            msg = DefineMpi.MPI_MESSAGE_DICT[msg_index]
            if not re.search(msg, self._current_output, re.IGNORECASE):
                found_all_messages = False
                self._logger.info("Failed: could not find expected message: " + msg)
                test_case_passed = False
            else:
                self._logger.info("Passed: found expected message: " + msg)
        if found_all_messages:
            self._logger.info("Passed: found all expected messages")
            
        if test_case_passed:
            if test_case_type == DefineMpi.TEST_TYPE_NEGATIVE:
                found_negative_message = False
                for msg_index in msg_list:
                    if msg_index in DefineMpi.MPI_NEGATIVE_MESSAGE_LIST:
                        found_negative_message = True
                        self._logger.info("Passed: found negative message: " + DefineMpi.MPI_MESSAGE_DICT[msg_index])
                        break
                if not found_negative_message:
                    test_case_passed = False
            
        if self.mpi_run_has_error():
            if test_case_type == DefineMpi.TEST_TYPE_POSITIVE:
                self._logger.error("Failed: found error message")
                test_case_passed = False
            else:
                self._logger.info("Passed: found error message")
        if self.mpi_run_has_aborted():
            if test_case_type == DefineMpi.TEST_TYPE_POSITIVE:
                self._logger.error("Failed: found abort message")
                test_case_passed = False
            else:
                self._logger.info("Passed: found abort message")
                    
        if cmd != DefineMpi.MPI_CMD_PINGPONG:
            for host_name, equal_result in self._vf_used_count_equal_dict.items():
                if not equal_result and test_case_type == DefineMpi.TEST_TYPE_POSITIVE:
                    self._logger.error("Failed: used vf count is not correct in host " + host_name)
                    test_case_passed = False
                    break
                    
        return test_case_passed
    
    
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
        if re.search(DefineMpi.MPI_MESSAGE_NOT_ENOUGH_USNIC, self._current_output, re.IGNORECASE):
            return True
        else:
            return False
        
        
    def mpi_run_not_enough_core(self):
        if re.search(DefineMpi.MPI_MESSAGE_NOT_ENOUGH_CORE, self._current_output, re.IGNORECASE):
            return True
        else:
            return False
        
        