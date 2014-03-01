'''
Created on Feb 27, 2014

@author: huhe
'''

import json
from pprint import pprint

from main_ucsm.define import Define
from main_ucsm.define_mpi import DefineMpi
from lib.logger import MyLogger
from lib.util import Util
from lib.ucsm_server import UcsmServer



if __name__ == '__main__':
    log = MyLogger.getLogger("create_run_mpi")
    
    path_vnic_default_json_file     = Define.PATH_TEST_CASE_UCSM + "vnic_default.json"
    path_create_run_mpi_json_file   = Define.PATH_TEST_CASE_UCSM + "create_run_mpi.json"
    
    vnic_default_data = json.load(open(path_vnic_default_json_file))
    #log.debug(vnic_default_data)
    test_case_data = json.load(open(path_create_run_mpi_json_file))
    #log.debug(test_case_data)
    
    ucsm_server_list = UcsmServer.init_ucsm_server(Define.UCSM_HOSTNAME)
    
    for test_case in test_case_data:
        test_case_name = test_case['name']
        node_count = test_case['node count']
        node_list = test_case['nodes']
        node_list = Util.populate_node_list(node_count, node_list)
        pprint(node_list)
        
        if len(node_list) <= len(ucsm_server_list):
            i = 0
            for node in node_list:
                ucsm_server = ucsm_server_list[i]
                ucsm_server.get_all_vnics_attributes()
                ucsm_server.delete_all_vnics()
                ucsm_server.configure(node, vnic_default_data)
                i += 1
        
        break
    
    '''
    ucsm_server_list = UcsmServer.init_ucsm_server(Define.UCSM_HOSTNAME)
    for ucsm_server in ucsm_server_list:
        ucsm_server.get_all_vnics_attributes()
        ucsm_server.delete_all_vnics()
    '''
        
        