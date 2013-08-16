'''
Created on Aug 14, 2013

@author: huhe
'''

from lib.util import Util


class Base(object):
    '''
    classdocs
    '''


    def __init__(self, ssh):
        '''
        Constructor
        '''
        self._logger = Util.getLogger(self.__class__.__name__)
        
        '''
        cimc: ssh session to rack server cimc
        ucsm: ssh session to ucsm
        '''
        self._ssh = ssh
        
        
    ### sendline and expect prompt wrapper
    def send_expect_prompt(self, cmd, timeout=None):
        self._ssh.send_expect_prompt(cmd, timeout)
        
        
    def get_output(self):
        return self._ssh.get_output()
    
    
    def exit(self):
        self._ssh.send("exit")

    
    
    