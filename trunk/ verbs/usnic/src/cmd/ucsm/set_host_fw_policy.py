'''
Created on Aug 21, 2013

@author: huhe
'''

from main.define import Define
from lib.ucsm_server import UcsmServer


if __name__ == '__main__':
    
    host_fw_policy_name = "default"
    
    ucsm_server_list = UcsmServer.init_ucsm_server(Define.UCSM_HOSTNAME)
    for ucsm_server in ucsm_server_list:
        
        if ucsm_server._chassis_index != 99:
            ucsm_server.scope_service_profile_from_top()
            ucsm_server.set_host_fw_policy(host_fw_policy_name)
            ucsm_server.show_host_fw_policy_brief()
    
