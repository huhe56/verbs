'''
Created on Aug 14, 2013

@author: huhe
'''

from main.define import Define
from lib.redhat import RedHat


class NodeHead(RedHat):
    '''
    classdocs
    '''


    def __init__(self, hostname, username=Define.NODE_USERNAME_ROOT, password=Define.NODE_DEFAULT_PASSWORD):
        '''
        Constructor
        '''
        RedHat.__init__(self, hostname, username, password)
        
        
        