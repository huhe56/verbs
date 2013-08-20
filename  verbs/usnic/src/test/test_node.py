'''
Created on Aug 8, 2013

@author: huhe
'''

from main.define import Define
from lib.util import Util
from lib.node_compute import NodeCompute
from lib.node_head import NodeHead


if __name__ == '__main__':
    
    head_node = NodeHead("10.193.212.18", "huhe")
    
    '''
    file_json_step = Define.PATH_USNIC_JSON_LINUX + "wget_ucsm_firmware.json"   
    Util.run_step_list(head_node.get_ssh(), file_json_step)
    '''
    
    
    compute_node = NodeCompute("node01")
    compute_node.send_expect_prompt("ls")
    compute_node.send_expect_prompt("pwd")
    eth_if_list = compute_node.get_eth_if_list()
    print eth_if_list
    compute_node._ssh.send("exit")
    
    
    
    
    
    
    
    