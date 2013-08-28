'''
Created on Aug 21, 2013

@author: huhe
'''

import time

from main.define import Define
from lib.ucsm import UCSM
from lib.ucsm_server import UcsmServer


if __name__ == '__main__':
    
    ucsm_server_list = UcsmServer.init_ucsm_server(Define.UCSM_HOSTNAME)
    '''
    power off all servers, wait for 60 seconds, power on all servers
    '''
    '''
    for i in range(0, 5):
        for ucsm_server in ucsm_server_list:
            ucsm_server.scope_service_profile_from_top()
            ucsm_server.power_off()
        time.sleep(60)
        for ucsm_server in ucsm_server_list:
            ucsm_server.scope_service_profile_from_top()
            ucsm_server.power_on()
        time.sleep(120)
    '''
        
    '''
    reboot only one server
    '''
    for ucsm_server in ucsm_server_list:
        if not ucsm_server._chassis_index and ucsm_server._server_index == 1:
            ucsm_server.scope_service_profile_from_top()
            ucsm_server.power_off()
            time.sleep(60)
            ucsm_server.power_on()
            time.sleep(120)
        
        
            