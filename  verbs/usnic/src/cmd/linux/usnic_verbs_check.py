'''
Created on Aug 21, 2013

@author: huhe
'''

from main import define
from main.define import Define
from lib.util import Util
from lib.node_compute import NodeCompute

if __name__ == '__main__':
    
    define.PEXPECT_OUTPUT_STDOUT = True
    
    path_config_file = Define.PATH_USNIC_CONFIG + "ping.cfg"
    node_name_list = Util.get_node_name_list(path_config_file)
    print node_name_list
    
    for node_name in node_name_list:
        node = NodeCompute(node_name)
        print "\n -------- "
        print node_name + " ----------"
        node.usnic_verbs_check()
        node.exit_ssh()
        
