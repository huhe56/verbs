'''
Created on Aug 14, 2013

@author: huhe
'''

from main.define import Define
from lib.redhat import RedHat

class ComputeNode(RedHat):
    '''
    classdocs
    '''


    def __init__(self, head_node, hostname, username=Define.NODE_DEFAULT_ROOT, password=Define.NODE_DEFAULT_PASSWORD):
        '''
        Constructor
        '''
        RedHat.__init__(self, hostname, username, password, head_node._ssh)
        
        self._head_node     = head_node        
        self._ssh.send_expect_prompt("ssh " + hostname)
        self._eth_if_list = self.find_eth_list()
        
        
    def send_expect_prompt(self, cmd, timeout=None):
        self._ssh.send_expect_prompt(cmd, timeout)
        
        
        