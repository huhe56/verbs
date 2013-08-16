'''
Created on Aug 8, 2013

@author: huhe
'''


from lib.node_compute import NodeCompute


if __name__ == '__main__':
    
    '''
    head_node = NodeHead("10.193.212.18", "huhe")
    head_node.send_expect_prompt("ls -l")
    head_node.send_expect_prompt("pwd")
    head_node._ssh.send("exit")
    '''
    
    compute_node = NodeCompute("node01")
    compute_node.send_expect_prompt("ls")
    compute_node.send_expect_prompt("pwd")
    eth_if_list = compute_node.get_eth_list()
    print eth_if_list
    compute_node._ssh.send("exit")
    
    
    
    
    
    
    