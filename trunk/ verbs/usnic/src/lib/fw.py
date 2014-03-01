'''
Created on Aug 13, 2013

@author: huhe
'''

from main import define
from main.define import Define
from lib.base import Base

'''
super class for cimc and ucsm server
'''
class FW(Base):
    '''
    classdocs
    '''


    def __init__(self, ssh):
        '''
        Constructor
        '''
        Base.__init__(self, ssh)
    

    def commit(self):
        self._ssh.send_expect_prompt("commit", Define.TIMEOUT_COMMIT)
        
        
    def scope_top(self):
        self._ssh.send_expect_prompt("top")
        
        
    def scope_chassis(self, chassis_index=None):
        if chassis_index:
            self._ssh.send_expect_prompt("scope chassis " + str(chassis_index))
        else:
            self._ssh.send_expect_prompt("scope chassis")
        
        
    def scope_server(self, server_index):
        self._ssh.send_expect_prompt("scope server " + str(server_index))
        
        
    def scope_adapter(self, adapter_index):
        self._ssh.send_expect_prompt("scope adapter " + str(adapter_index))
        
    
    def scope_host_eth_if(self, host_eth_if):
        self._ssh.send_expect_prompt("scope host-eth-if " + host_eth_if)
    
    
    def scope_chassis_from_top(self, chassis_index=None):
        self.scope_top()
        self.scope_chassis(chassis_index)
        
        
    def scope_adapter_from_top(self, adapter_index):
        pass
    
    
    def scope_host_eth_if_from_top(self, adapter_index, host_eth_if):
        pass
    
    
    def scope_usnic_from_top(self, adapter_index, host_eth_if):
        pass
    

    
        
        