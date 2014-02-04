'''
Created on Aug 19, 2013

@author: huhe
'''

import sys
import pprint
import ipaddr
import Queue, threading, time

from main import define
from main.define import Define
from lib.util import Util
from lib.node_compute import NodeCompute


def start_pingpong_server(q, server_ip, server_usnic):
    server_node_name = Util.find_node_name_by_ip("bcnode", server_ip)
    print "\n------------> server: " + server_node_name
    server_node = NodeCompute(server_node_name)
    ssh = server_node.get_ssh()
    if not ssh:
        print "Failed to ssh to server " + server_node_name
        q.put(False)
    else:
        server_ret = server_node.start_pingpong_server(server_usnic)
        q.put(server_ret)
    
    
def start_pingpong_client(client_ip, client_usnic, server_ip):
    client_node_name = Util.find_node_name_by_ip("bcnode", client_ip)
    print "\n------------> client: " + client_node_name
    node = NodeCompute(client_node_name)
    ssh = node.get_ssh()
    if not ssh:
        print "Failed to ssh to client " + client_node_name
        return False
    else:
        ret = node.start_pingpong_client(usnic, server_ip)
        return ret
    
    
if __name__ == '__main__':
    
    define.PEXPECT_OUTPUT_STDOUT = False
    
    if len(sys.argv) == 3:
        node_usr = sys.argv[1]
        node_pwd = sys.argv[2]
    else:
        node_usr = Define.NODE_DEFAULT_USERNAME
        node_pwd = Define.NODE_DEFAULT_PASSWORD
    
    path_config_file = Define.PATH_USNIC_CONFIG + "ping.cfg"
    node_name_list = Util.get_node_name_list(path_config_file)
    print node_name_list

    node_list = []
    subnet_dict = {}
    for node_name in node_name_list:
        node = NodeCompute(node_name, node_usr, node_pwd)
        node_list.append(node)
        if node.get_ssh(): 
            usnic_index = 0
            eth_if_list = node.get_usnic_eth_if_ip_list()
            node.exit_ssh()
            for eth_if in eth_if_list:
                if eth_if.startswith("127.") or eth_if.startswith("192.168."): continue
                subnet = str(ipaddr.IPv4Network(eth_if + "/24").network)
                if subnet not in subnet_dict.keys():
                    subnet_dict[subnet] = {}
                subnet_dict[subnet][eth_if] = 'usnic_' + str(usnic_index)
                usnic_index = usnic_index + 1
            
                
    pprint.pprint(subnet_dict)
    
    
    print "\n"
    for subnet, usnic_ip_dict in subnet_dict.iteritems():
        print "total ip addresses in subnet " + subnet + ": " + str(len(usnic_ip_dict))
    print "\n"
    
    #define.PEXPECT_OUTPUT_STDOUT = True
    
    total_passed = 0
    total_failed = 0
    for subnet, usnic_ip_dict in subnet_dict.iteritems():
        index = 0
        server_ip = None
        server_usnic = None
        for ip_address, usnic in usnic_ip_dict.iteritems():
            if index == 0:
                server_ip = ip_address
                server_usnic = usnic
                index = index + 1
            else:
                q = Queue.Queue()
                t = threading.Thread(target=start_pingpong_server, args=(q, server_ip, server_usnic))
                t.daemon = True
                t.start()
                
                time.sleep(2)
                
                client_ret = start_pingpong_client(ip_address, usnic, server_ip)
                
                server_ret = q.get()
                
                if server_ret and client_ret:
                    print "Passed: " + server_ip + " -> " + ip_address
                    total_passed = total_passed + 1
                else:
                    print "Failed: " + server_ip + " -> " + ip_address
                    total_failed = total_failed + 1
            
                time.sleep(10)
                
    print "\n\n== full mash pingpong result =="
    print "Total passed: " + str(total_passed)
    print "Total failed: " + str(total_failed)
    print "\n"
    