'''
Created on Aug 13, 2013

@author: huhe
'''

import re 

from main.define import Define
from lib.ssh import SSH
from lib.fw import FW


class CIMC(FW):
    '''
    classdocs
    '''


    def __init__(self, hostname, username=Define.CIMC_DEFAULT_USERNAME, password=Define.CIMC_DEFAULT_PASSWORD):
        '''
        Constructor
        '''
        self._hostname = hostname
        self._username = username
        self._password = password
        FW.__init__(self, SSH(hostname, username, password))
        
        
    def scope_usnic(self):
        self.send_expect_prompt("scope usnic-config 0")
        
        
    def scope_adapter_from_top(self, adapter_index):
        self.scope_top()
        self.scope_chassis()
        self.scope_adapter(adapter_index)
        
        
    def scope_usnic_from_top(self, adapter_index, host_eth_if):
        self.scope_adapter_from_top(adapter_index)
        self.scope_host_eth_if(host_eth_if)
        self.scope_usnic()
        
    
    def create_usnic(self, host_eth_if, count):
        self._ssh.send_expect_prompt("create host-eth-if " + host_eth_if)
        self.commit()
        self._ssh.send_expect_prompt("create usnic-config 0")
        self.set_count(count)
        
        
    def delete_usnic(self, host_eth_if):
        self._ssh.send_expect_prompt("delete host-eth-if " + host_eth_if)
        self.commit()
        
        
    def show_usnic_detail(self):
        self._ssh.send_expect_prompt("show detail")
        
        
    def show_usnic_brief(self):
        self._ssh.send_expect_prompt("show")
        
        
    def set_usnic_count(self, count):
        self._ssh.send_expect_prompt("set usnic-count " + str(count))
        self.commit()
        
        
    def get_usnic_count(self):
        self.get_usnic_brief()
        output = self.get_output()
        lines = output.split(Define.PATTERN_NEW_LINE)
        items = re.compile("\s+").split(lines[3])
        return items[1]
    
        
        
    
