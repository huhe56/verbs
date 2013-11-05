'''
Created on Aug 8, 2013

@author: huhe
'''
import time

from main.define import Define
from lib.util import Util
from lib.node_compute import NodeCompute
from lib.node_head import NodeHead


if __name__ == '__main__':
    
    #head_node = NodeHead("10.193.212.18", "huhe")
    
    
    #file_json_step = Define.PATH_USNIC_JSON_LINUX + "wget_ucsm_firmware.json"   
    #Util.run_step_list(head_node.get_ssh(), file_json_step)
    
    
    '''
    compute_node = NodeCompute("node01")
    compute_node.send_expect_prompt("ls")
    compute_node.send_expect_prompt("pwd")
    eth_if_list = compute_node.get_eth_if_list()
    print eth_if_list
    compute_node._ssh.send("exit")
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
    
    
    
    
    
    