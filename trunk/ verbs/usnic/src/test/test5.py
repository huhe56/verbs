'''
Created on Aug 8, 2013

@author: huhe
'''


from lib.head_node import HeadNode
from lib.compute_node import ComputeNode


if __name__ == '__main__':
    
    head_node = HeadNode("10.193.212.18", "huhe")
    
    head_node._ssh.send_expect_prompt("ls")
    #head_node._ssh.send("exit")
    
    compute_node = ComputeNode(head_node, "node01")
    
    #compute_node.send_expect_prompt("ls")
    #compute_node.send_expect_prompt("pwd")
    compute_node.send_expect_prompt("exit\n")
    
    head_node._ssh.send("exit")
    
    
    
    
    