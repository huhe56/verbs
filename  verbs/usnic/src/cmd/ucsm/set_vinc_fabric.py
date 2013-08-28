'''
Created on Aug 21, 2013

@author: huhe
'''

from main.define import Define
from lib.ucsm_server import UcsmServer


if __name__ == '__main__':
    
    ucsm_server_list = UcsmServer.init_ucsm_server(Define.UCSM_HOSTNAME)
    for ucsm_server in ucsm_server_list:
        
        ucsm_server.scope_vnic_from_top("eth-10")
        ucsm_server.set_vnic_fabric("a")
        ucsm_server.scope_vnic_from_top("eth-20")
        ucsm_server.set_vnic_fabric("b")
        
        ucsm_server.show_vnic_brief("eth-10")
        ucsm_server.show_vnic_brief("eth-20")
    
