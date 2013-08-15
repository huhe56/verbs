'''
Created on Aug 14, 2013

@author: huhe
'''

from main.define import Define
from lib.redhat import RedHat
from lib.ssh import SSH


class HeadNode(RedHat):
    '''
    classdocs
    '''


    def __init__(self, hostname, username=Define.NODE_DEFAULT_ROOT, password=Define.NODE_DEFAULT_PASSWORD):
        '''
        Constructor
        '''
        RedHat.__init__(self, hostname, username, password)
        
        self._ssh = SSH(hostname, username, password)
        