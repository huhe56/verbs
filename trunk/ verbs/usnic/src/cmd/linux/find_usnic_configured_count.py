'''
Created on Aug 21, 2013

@author: huhe
'''

from main import define
from main.define import Define
from lib.util import Util
from lib.node_compute import NodeCompute

if __name__ == '__main__':
    
    define.PEXPECT_OUTPUT_STDOUT = False
    
    path_config_file = Define.PATH_USNIC_CONFIG + "ping.cfg"
    node_name_list = Util.get_node_name_list(path_config_file)
    print node_name_list
    
    for node_name in node_name_list:
        node = NodeCompute(node_name)
        count_list = node.get_usnic_configured_count_list()
        node.exit_ssh()
        print node_name
        print count_list 