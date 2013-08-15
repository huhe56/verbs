'''
Created on Aug 13, 2013

@author: huhe
'''

from main.define import Define
from lib.ssh import SSH
from lib.usnic import USNIC


class CIMC(USNIC):
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
        self._ssh = SSH(hostname, username, password)
        USNIC.__init__(self, self._ssh)
        
    
    def scope_adapter_from_top(self, adapter_index):
        self.scope_top()
        self.scope_chassis()
        self.scope_adapter(adapter_index)
        
        
    def scope_usnic_from_top(self, adapter_index, host_eth_if):
        self.scope_top()
        self.scope_chassis()
        self.scope_adapter(adapter_index)
        self.scope_host_eth_if(host_eth_if)
        self.scope_usnic()
        
        
        
        
        
    
