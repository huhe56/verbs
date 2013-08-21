'''
Created on Aug 8, 2013

@author: huhe
'''


from main.define import Define
from lib.ucsm import UCSM
from lib.ucsm_server import UcsmServer


if __name__ == '__main__':
    
    
    ucsm_server_list = UcsmServer.init_ucsm_server(Define.UCSM_HOSTNAME)
    for ucsm_server in ucsm_server_list:
        output = ucsm_server.show_cpu_brief()
        print ucsm_server._service_profile
    
    
    ucsm = UCSM(Define.UCSM_HOSTNAME);
    print "\n--------\n" + ucsm.show_cpu_brief()
    
    
    
    
    
    