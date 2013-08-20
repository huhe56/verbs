'''
Created on Aug 19, 2013

@author: huhe
'''

import pprint
import ipaddr

from main.define import Define
from lib.util import Util
from lib.node_compute import NodeCompute

    
if __name__ == '__main__':
    path_config_file = Define.PATH_USNIC_CONFIG + "ping.cfg"
    node_name_list = Util.get_node_name_list(path_config_file)
    print node_name_list

    node_list = []
    subnet_dict = {}
    for node_name in node_name_list:
        node = NodeCompute(node_name)
        node_list.append(node)
        if node.get_ssh(): 
            eth_if_list = node.get_eth_if_list()
            for eth_if in eth_if_list:
                if eth_if.startswith("127.") or eth_if.startswith("192.168."): continue
                subnet = str(ipaddr.IPv4Network(eth_if + "/24").network)
                if subnet not in subnet_dict.keys():
                    subnet_dict[subnet] = []
                subnet_dict[subnet].append(eth_if)
                
    pprint.pprint(subnet_dict)
    print "\n"
    
    summary = [0, 0, 0, 0]
    for node in node_list:
        ssh = node.get_ssh()
        if not ssh:
            summary[1] = summary[1] + 1
            print "Error: can't ssh to " + node._hostname
        else:
            summary[0] = summary[0] + 1
            eth_if_list = node.get_eth_if_list()
            for eth_if in eth_if_list:
                subnet = str(ipaddr.IPv4Network(eth_if + "/24").network)
                if subnet in subnet_dict.keys():
                    subnet_ip_list = subnet_dict[subnet]
                    for ip in subnet_ip_list:
                        status = Util.ping(ssh, ip, 2)
                        if status:
                            summary[2] = summary[2] + 1
                            print "Passed: ping " + ip + " from " + eth_if
                        else:
                            summary[3] = summary[3] + 1
                            print "Failed: ping " + ip + " from " + eth_if
                         
    print "\n\n== full mash ping result =="
    for i in summary:
        if i == 0:
            print "total node(s) can be ssh'ed to: " + summary[i]
        elif i == 1:
            print "total node(s) can not be ssh'ed to: " + summary[i]
        elif i == 2:
            print "total ping(s) successful: " + summary[i]
        elif i == 3:
            print "total ping(s) failed: " + summary[i]
        