'''
Created on Aug 13, 2013

@author: huhe
'''

from lib.usnic import USNIC


class UcsmBlade(USNIC):
    '''
    classdocs
    '''


    def __init__(self, ucsm, chassis_index, server_index):
        '''
        Constructor
        '''
        self._ucsm = ucsm
        self._chassis_index = chassis_index
        self._server_index = server_index
        USNIC.__init__(self, ucsm.get_ssh())
        
    
    def scope_adapter_from_top(self, adapter_index):
        self.scope_top()
        self.scope_chassis(self._chassis_index)
        self.scope_server(self.server_index)
        self.scope_adapter(adapter_index)
        
        
    def scope_usnic_from_top(self, adapter_index, host_eth_if):
        self.scope_top()
        self.scope_chassis(self._chassis_index)
        self.scope_server(self._server_index)
        self.scope_adapter(adapter_index)
        self.scope_host_eth_if(host_eth_if)
        self.scope_usnic()
        
        
