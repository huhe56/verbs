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
    
    start_script = True
    
    path_config_file = Define.PATH_USNIC_CONFIG + "ping.cfg"
    node_name_list = Util.get_node_name_list(path_config_file)
    print node_name_list
    for node_name in node_name_list:
        print node_name
        node = NodeCompute(node_name)
        if start_script:
            node._ssh.send_expect_prompt('rm /tmp/ps-output.txt')
            node._ssh.send_expect_prompt('rm /tmp/time-to-quit')
            node._ssh.send_expect_prompt('/home/huhe/shell/misc/ps.sh &')
        else:
            node._ssh.send_expect_prompt('touch /tmp/time-to-quit')
        node.exit_ssh()
        
