'''
Created on Aug 14, 2013

@author: huhe
'''

from lib.base import Base
from lib.ssh import SSH


class RedHat(Base):
    '''
    classdocs
    '''


    def __init__(self, hostname, username, password):
        '''
        Constructor
        '''        
        self._hostname = hostname
        self._username = username
        self._password = password
        Base.__init__(self, SSH(hostname, username, password))
        self._eth_if_list = None
        
        
    def get_eth_if_list(self):
        if not self._eth_if_list:
            self._eth_if_list = self._ssh.send_match_list("ifconfig", "(?<=inet addr:)(?:\d{1,3}\.){3}\d{1,3}")
        return self._eth_if_list
        
        
    def start_ssh(self):
        ssh = SSH(self._hostname, self._username, self._password)
        self.set_ssh(ssh)
        
        
        