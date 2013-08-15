'''
Created on Aug 14, 2013

@author: huhe
'''

import re

from lib.util import Util
from lib.ssh import SSH


class RedHat(object):
    '''
    classdocs
    '''


    def __init__(self, hostname, username, password):
        '''
        Constructor
        '''
        self._logger = Util.getLogger(self.__class__.__name__)
        
        self._hostname = hostname
        self._username = username
        self._password = password
        self._ssh = SSH(hostname, username, password)
        
        self._eth_if_list = None
        
        
    def send_expect_prompt(self, cmd, timeout=None):
        self._ssh.send_expect_prompt(cmd, timeout)
        
        
    def get_eth_list(self):
        if not self._eth_if_list:
            self._eth_if_list = self._ssh.send_match_list("ifconfig", "(?<=inet addr:)(?:\d{1,3}\.){3}\d{1,3}")
        return self._eth_if_list
        
        
    
        