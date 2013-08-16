'''
Created on Aug 13, 2013

@author: huhe
'''

from main.define import Define
from lib.ssh import SSH


class UCSM(object):
    '''
    classdocs
    '''


    def __init__(self, hostname, username=Define.UCSM_DEFAULT_USERNAME, password=Define.UCSM_DEFAULT_PASSWORD):
        '''
        Constructor
        '''
        self._hostname = hostname
        self._username = username
        self._password = password
        self._ssh = SSH(hostname, username, password)

    
    def get_ssh(self):
        return self._ssh
    
    
    def scope_top(self):
        self._ssh.send_expect_prompt("terminal length 0")
        self._ssh.send_expect_prompt("top")
        
        
    def show_cup_brief(self):
        self.scope_top()
        self._ssh.send_expect_prompt("show server cpu")
        return self._ssh.get_output()
        
        
        
        
    
