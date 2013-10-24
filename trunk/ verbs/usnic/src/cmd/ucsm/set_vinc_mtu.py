'''
Created on Aug 21, 2013

@author: huhe
'''

from main.define import Define
from lib.ucsm_server import UcsmServer


if __name__ == '__main__':
    
    vnic_policy_type    = Define.VNIC_MTU
    vnic_policy_label   = Define.VNIC_MTU_LABEL
    vnic_policy_name    = "1500"
    vnic_list = ["eth-10", "eth-20"]
    
    ucsm_server_list = UcsmServer.init_ucsm_server(Define.UCSM_HOSTNAME)
    for ucsm_server in ucsm_server_list:
        
        if ucsm_server._chassis_index != 99 and ucsm_server._server_index != 99:
            for vnic_name in vnic_list:
                ucsm_server.set_vnic_policy(vnic_name, vnic_policy_type, vnic_policy_name)
                ucsm_server.show_vnic_policy(vnic_name, vnic_policy_label)
    
