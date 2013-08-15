'''
Created on Aug 14, 2013

@author: huhe
'''

import re, time

from lib.util import Util


class RedHat(object):
    '''
    classdocs
    '''


    def __init__(self, hostname, username, password, ssh=None):
        '''
        Constructor
        '''
        self._logger = Util.getLogger(self.__class__.__name__)
        
        self._hostname = hostname
        self._username = username
        self._password = password
        self._ssh = ssh
        
        
    def find_eth_list(self):
        
        self._ssh.send_expect_prompt("ifconfig")
        ''' wired workaround '''
        self._ssh.send_expect_prompt("")
        output = self._ssh.get_output()
        self._logger.debug(output)
        pattern = re.compile("(?<=inet addr:)(?:\d{1,3}\.){3}\d{1,3}")
        match_list = pattern.findall(output)
        self._logger.debug(match_list)
        return match_list
        
        