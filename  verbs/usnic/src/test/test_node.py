'''
Created on Aug 8, 2013

@author: huhe
'''
import time

from main import define
from main_ucsm.define import Define
from main_ucsm.define_mpi import DefineMpi
from lib.util import Util
from lib.node_compute import NodeCompute
from lib.node_head import NodeHead


if __name__ == '__main__':
    
    #head_node = NodeHead("10.193.212.18", "huhe")
    
    
    #file_json_step = Define.PATH_USNIC_JSON_LINUX + "wget_ucsm_firmware.json"   
    #Util.run_step_list(head_node.get_ssh(), file_json_step)
    
    host = NodeCompute("node03")
    host.get_usnic_status_data()
    
    host.get_ifconfig_data()
    
    #compute_node = NodeCompute.wait_for_node_to_boot_up("192.168.42.2")
    
    #compute_node.send_expect_prompt("ls")
    #compute_node.send_expect_prompt("pwd")
    #eth_if_list = compute_node.get_usnic_eth_if_ip_list()
    #print eth_if_list
    #compute_node._ssh.send("exit")
    
    '''
    node = None
    probe_max_count = 10
    try_count = 1
    interval = 60
    while try_count <= probe_max_count:
        node = NodeCompute("bcnode01")
        if not node.get_ssh():
            Util._logger.info("probe times: " + str(try_count))
            time.sleep(interval)
            try_count = try_count + 1
        else:
            break
    
    eth_if_list = node.get_eth_if_name_list()
    print eth_if_list
    
    ret = node._ssh.send_match_list("/opt/cisco/usnic/bin/usnic_status", "(?:\d+)\sVFs")
    print ret 
    
    ret = node.get_usnic_configured_count_list()
    print ret 
    
    ret = node.get_usnic_used_count_list()
    print ret 
    '''
    '''
    define.PEXPECT_OUTPUT_STDOUT = False
    host = NodeCompute("bcnode13")
    params = {
            #DefineMpi.MPI_PARAM_CMD:                    DefineMpi.MPI_CMD_PINGPONG,
            DefineMpi.MPI_PARAM_HOST:                   ["bcnode13", "bcnode14"],
            #DefineMpi.MPI_PARAM_CHECK_VF_USED_COUNT:    True,
            #DefineMpi.MPI_PARAM_VF_USED_COUNT_LIST:     [16, 16, 16, 16, 16, 16]
            }
    
    host.run_mpi(params)
    '''
    
    
    
    
    