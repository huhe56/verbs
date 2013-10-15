'''
Created on Aug 21, 2013

@author: huhe
'''

from main.define import Define
from lib.ucsm_server import UcsmServer


if __name__ == '__main__':
    
    boot_policy_name = "pxe-boot-only"
    
    ucsm_server_list = UcsmServer.init_ucsm_server(Define.UCSM_HOSTNAME)
    for ucsm_server in ucsm_server_list:
        
        '''
        don't do chassis 4, they are pxe, iscsi and fc, which is different boot policy
        '''
        if ucsm_server._chassis_index != 4:
            ucsm_server.scope_service_profile_from_top()
            ucsm_server.set_boot_policy(boot_policy_name)
            ucsm_server.show_boot_policy_brief()
    
