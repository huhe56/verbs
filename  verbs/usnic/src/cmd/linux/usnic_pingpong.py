'''
Created on Aug 21, 2013

@author: huhe
'''

import re
from main import define
from main.define import Define
from lib.util import Util
from lib.node_compute import NodeCompute

server_node_ip = 'bcnode01'
server_usnic_number = 0
server_usnic_ip = '50.35.10.101'

usnic_ip_list =[
                '50.35.10.102',
                '50.35.10.105',
                '50.35.10.106',
                '50.35.10.107',
                '50.35.10.108',
                '50.35.10.109',
                '50.35.10.110',
                '50.35.10.113',
                '50.35.10.114',
                '50.35.10.116',
                '50.35.10.117',
                '50.35.10.118',
                '50.35.10.119',
                '50.35.10.121',
                '50.35.10.125',
                '50.35.10.141',
                '50.35.10.142',
                '50.35.10.143',
                '50.35.10.144',
                '50.35.10.145',
                '50.35.10.146',
                '50.35.10.147',
                '50.35.10.148',
                '50.35.10.149',
                '50.35.10.152',
                '50.35.10.153',
                '50.35.10.154',
                '50.35.10.157',
                '50.35.10.159',
                '50.35.10.160',
                '50.35.10.161',
                '50.35.10.162',
                '50.35.10.165',
                '50.35.10.166',
                '50.35.10.167',
                '50.35.10.168']

if __name__ == '__main__':
    
    define.PEXPECT_OUTPUT_STDOUT = True
    
    path_config_file = Define.PATH_USNIC_CONFIG + "ping.cfg"
    node_name_list = Util.get_node_name_list(path_config_file)
    print node_name_list
    
    count = 0
    for usnic_ip in usnic_ip_list:
        item_list = usnic_ip.split(".")
        node_number = re.sub('^1', '', item_list[3])
        node_name = 'bcnode' + node_number
        print node_name
        count = count + 1
        
        node = NodeCompute(node_name)
        node.usnic_pingpong(0, '50.35.10.101')
        node.exit_ssh()
        
    print "total: " + str(count)
    
        
