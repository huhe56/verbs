'''
Created on Aug 13, 2013

@author: huhe
'''

import re

from main.define import Define
from lib.base import Base


class USNIC(Base):
    '''
    classdocs
    '''


    def __init__(self, ssh):
        '''
        Constructor
        '''
        Base.__init__(self, ssh)
        
        
    def get_output(self):
        return self._ssh.get_output()
    
    
    def exit(self):
        self._ssh.send("exit")


    ### sendline and expect prompt wrapper
    def send_expect_prompt(self, cmd, timeout=None):
        self._ssh.send_expect_prompt(cmd, timeout)
        
        
    def commit(self):
        self.send_expect_prompt("commit", Define.TIMEOUT_COMMIT)
        
        
    def scope_top(self):
        self.send_expect_prompt("top")
        
        
    def scope_chassis(self, chassis_index=None):
        if chassis_index:
            self.send_expect_prompt("scope chassis " + str(chassis_index))
        else:
            self.send_expect_prompt("scope chassis")
        
        
    def scope_server(self, server_index):
        self.send_expect_prompt("scope server " + str(server_index))
        
        
    def scope_adapter(self, adapter_index):
        self.send_expect_prompt("scope adapter " + str(adapter_index))
        
    
    def scope_host_eth_if(self, host_eth_if):
        self.send_expect_prompt("scope host-eth-if " + host_eth_if)
    
    
    def scope_usnic(self):
        self.send_expect_prompt("scope usnic-config 0")
        
    
    def scope_chassis_from_top(self):
        pass
        
        
    def scope_adapter_from_top(self, adapter_index):
        pass
    
    
    def scope_host_eth_if_from_top(self, adapter_index, host_eth_if):
        pass
    
    
    def scope_usnic_from_top(self, adapter_index, host_eth_if):
        pass
    
        
    def create(self, host_eth_if, count):
        self.send_expect_prompt("create host-eth-if " + host_eth_if)
        self.commit()
        self.send_expect_prompt("create usnic-config 0")
        self.set_count(count)
        
    
    def delete(self, host_eth_if):
        self.send_expect_prompt("delete host-eth-if " + host_eth_if)
        self.commit()
        
        
    def get_detail(self):
        self.send_expect_prompt("show detail")
        
        
    def get_brief(self):
        self.send_expect_prompt("show")
        
        
    def set_count(self, count):
        self.send_expect_prompt("set usnic-count " + str(count))
        self.commit()
        
        
    def get_count(self):
        self.get_brief()
        output = self.get_output()
        lines = output.split(Define.PATTERN_NEW_LINE)
        items = re.compile("\s+").split(lines[3])
        return items[1]
    
    
        
        