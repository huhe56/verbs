'''
Created on Aug 21, 2013

@author: huhe
'''

from main import define
from main.define import Define
from lib.util import Util
from lib.ssh import SSH


if __name__ == '__main__':
    
    define.PEXPECT_OUTPUT_STDOUT = False
    
    path_config_file = Define.PATH_USNIC_CONFIG + "ping.cfg"
    node_name_list = Util.get_node_name_list(path_config_file)
    print node_name_list
    
    ssh = SSH(Define.NODE_HEAD_NAME, Define.NODE_DEFAULT_USERNAME, Define.NODE_DEFAULT_PASSWORD)
    for node_name in node_name_list:
        status = Util.ping(ssh, node_name, 2)
        if status:
            print "Passed: " + node_name + " is up"
        else:
            print "Failed: " + node_name + " is down"