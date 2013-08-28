'''
Created on Aug 26, 2013

@author: huhe
'''

from main.define import Define
from lib.util import Util
from lib.node_head import NodeHead


if __name__ == '__main__':
    
    head_node = NodeHead(Define.NODE_HEAD_NAME, "huhe")
    
    file_json_step = Define.PATH_USNIC_JSON_LINUX + "wget_ucsm_firmware.json"   
    Util.run_step_list(head_node.get_ssh(), file_json_step)