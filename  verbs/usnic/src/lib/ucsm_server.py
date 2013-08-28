'''
Created on Aug 13, 2013

@author: huhe
'''

from main.define import Define
from lib.fw import FW
from lib.ucsm import UCSM


class UcsmServer(FW):
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
        FW.__init__(self, ucsm.get_ssh())
        
        self._service_profile = None
        
        
    @staticmethod
    def init_ucsm_server(ucsm_hostname):
        ucsm_server_list = []
        ucsm = UCSM(ucsm_hostname)
        for chassis_index in Define.UCSM_BLADE_SERVER_LIST:
            for server_index, service_profile in Define.UCSM_BLADE_SERVER_LIST[chassis_index].items():
                blade_server = UcsmServer(ucsm, chassis_index, server_index)
                blade_server.set_service_profile(service_profile)
                ucsm_server_list.append(blade_server)
        for server_index, service_profile in Define.UCSM_RACK_SERVER_LIST.items():
            rack_server = UcsmServer(ucsm, None, server_index)
            rack_server.set_service_profile(service_profile)
            ucsm_server_list.append(rack_server)
        return ucsm_server_list
    
    
    def scope_server_from_top(self):
        self.scope_top()
        if self._chassis_index:
            self.scope_chassis(self._chassis_index)
        self.scope_server(self._server_index)


    def show_cpu_brief(self):
        self.scope_server_from_top()
        self._ssh.send_expect_prompt("show cpu")
        self._logger.debug(self._ssh.get_output())
        
        
    def set_service_profile(self, service_profile):
        self._service_profile = service_profile
        
        
    def scope_service_profile_from_top(self):
        self._ssh.send_expect_prompt("top")
        self._ssh.send_expect_prompt("scope org")
        self._ssh.send_expect_prompt("scope service-profile " + self._service_profile)
        
        
    def scope_vnic_from_top(self, vnic_name):
        self.scope_service_profile_from_top()
        self._ssh.send_expect_prompt("scope vnic " + vnic_name)
        
    
    def show_vnic_brief(self, vnic_name):
        self.scope_vnic_from_top(vnic_name)
        self._ssh.send_expect_prompt("show")
        
        
    '''
    fabric string can be: a, a-b, b, b-a
    '''
    def set_vnic_fabric(self, fabric_string):
        self._ssh.send_expect_prompt("set fabric " + fabric_string)
        self.commit()
        
        
    def power_on(self):
        self._ssh.send_expect_prompt("power up")
        self.commit()
        
        
    def power_off(self):
        self._ssh.send_expect_prompt("power down")
        self.commit()
        
        
