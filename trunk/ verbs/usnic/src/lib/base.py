'''
Created on Aug 14, 2013

@author: huhe
'''

from lib.logger import MyLogger


class Base(object):
    '''
    classdocs
    '''


    def __init__(self, ssh):
        '''
        Constructor
        '''
        self._logger = MyLogger.getLogger(self.__class__.__name__)
        
        '''
        cimc: ssh session to rack server cimc
        ucsm: ssh session to ucsm
        '''
        self._ssh = None
        self.set_ssh(ssh)
        
        
    def get_ssh(self):
        return self._ssh
    
    
    def set_ssh(self, ssh):
        if ssh.is_login_ok():
            #self._logger.debug("login is ok and set in Base")
            self._ssh = ssh
            
            
    def exit_ssh(self):
        self._ssh.send("exit")
        self._ssh = None
    
    
    def exit(self):
        self.exit_ssh()
    

    
    
    