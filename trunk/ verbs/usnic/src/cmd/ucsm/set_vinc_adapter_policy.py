'''
Created on Aug 21, 2013

@author: huhe
'''

from main.define import Define
from lib.ucsm_server import UcsmServer


if __name__ == '__main__':
    
    vnic_adapter_policy_name = "Linux"
    vnic_list = ["eth-10", "eth-20"]
    
    ucsm_server_list = UcsmServer.init_ucsm_server(Define.UCSM_HOSTNAME)
    for ucsm_server in ucsm_server_list:
        
        if ucsm_server._chassis_index != 99 and ucsm_server._server_index != 99:
            for vnic in vnic_list:
                ucsm_server.scope_vnic_from_top(vnic)
                ucsm_server.set_vnic_adapter_policy(vnic_adapter_policy_name)
                ucsm_server.show_vnic_brief(vnic)
    
