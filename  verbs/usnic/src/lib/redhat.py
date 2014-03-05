'''
Created on Aug 14, 2013

@author: huhe
'''

import re

from main.define import Define
from lib.base import Base
from lib.ssh import SSH


class RedHat(Base):
    '''
    classdocs
    '''


    def __init__(self, hostname, username, password):
        '''
        Constructor
        '''        
        self._hostname = hostname
        self._username = username
        self._password = password
        Base.__init__(self, SSH(hostname, username, password))
        self._eth_if_list = None
        
        
    def get_host_name(self):
        return self._hostname
        
        
    def get_next_no_ip_eth_if_name_list(self, count):
        eth_if_name_list = self.get_eth_if_name_list()
        i = len(eth_if_name_list)
        last_eth_if_name = eth_if_name_list[i-1]
        last_eth_if_index = int(last_eth_if_name.replace("eth", ""))
        ret_list = ["eth" + str(last_eth_if_index + j) for j in range(1, count+1)]
        return ret_list
        
    
    def set_eth_if_ip(self, eth_if, ip_mask):
        self._ssh.send("su -")
        self._ssh.expect("assword: ")
        self._ssh.send_expect_prompt(Define.NODE_DEFAULT_PASSWORD)
        self._ssh.send_expect_prompt("ifconfig " + eth_if + " " + ip_mask + " up")
        self._ssh.send_expect_prompt("exit")
        
        
    def get_eth_if_list(self):
        if not self._eth_if_list:
            self._eth_if_list = self._ssh.send_match_list("ifconfig", "(?<=inet addr:)(?:\d{1,3}\.){3}\d{1,3}")
        return self._eth_if_list
    
    
    def get_eth_if_name_list(self):
        if not self._eth_if_list:
            self._eth_if_list = self._ssh.send_match_list("ifconfig", "(?:eth\d+)")
        return self._eth_if_list
    
    
    def get_shell_status(self):
        self._ssh.send("echo status=$?")
        self._ssh.expect("status=\d+")
        status_str = self._ssh.get_output()
        #self._logger.debug(status_str)
        match = re.search('(?<=status=)\d+', status_str)
        return int(match.group(0))
        
        
    def start_ssh(self):
        ssh = SSH(self._hostname, self._username, self._password)
        self.set_ssh(ssh)
        
        
    def set_mtu(self, eth_if, mtu):
        self._ssh.send("su -")
        self._ssh.expect("assword: ")
        self._ssh.send_expect_prompt(Define.NODE_DEFAULT_PASSWORD)
        self._ssh.send_expect_prompt("ifconfig " + eth_if + " mtu " + str(mtu))
        self._ssh.send_expect_prompt("exit")
        
    
    def show_ifconfig(self):
        self._ssh.send_expect_prompt("ifconfig")
        
        