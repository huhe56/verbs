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
    
        
        
        
        
        
    
