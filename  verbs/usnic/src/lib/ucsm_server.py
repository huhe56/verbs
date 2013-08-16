'''
Created on Aug 13, 2013

@author: huhe
'''

from main.define import Define
from lib.util import Util
from lib.usnic import USNIC
from lib.ucsm import UCSM


class UcsmServer(USNIC):
    '''
    classdocs
    '''


    def __init__(self, ucsm, chassis_index, server_index):
        '''
        Constructor
        '''
        self._logger = Util.getLogger(self.__class__.__name__)
        self._ucsm = ucsm
        self._chassis_index = chassis_index
        self._server_index = server_index
        USNIC.__init__(self, ucsm.get_ssh())
        
    
    @staticmethod
    def init_ucsm_server(ucsm_hostname):
        ucsm_server_list = []
        ucsm = UCSM(ucsm_hostname)
        for chassis_index in Define.UCSM_BLADE_SERVER_LIST:
            for server_index in Define.UCSM_BLADE_SERVER_LIST[chassis_index]:
                blade_server = UcsmServer(ucsm, chassis_index, server_index)
                ucsm_server_list.append(blade_server)
        for server_index in Define.UCSM_RACK_SERVER_LIST:
            rack_server = UcsmServer(ucsm, None, server_index)
            ucsm_server_list.append(rack_server)
        return ucsm_server_list
    
    
    def scope_server_from_top(self):
        self.scope_top()
        if self._chassis_index:
            self.scope_chassis(self._chassis_index)
        self.scope_server(self._server_index)


    def get_cpu_brief(self):
        self.scope_server_from_top()
        self.send_expect_prompt("show cpu")
        self._logger.debug(self.get_output())
        
        
    
        
        
