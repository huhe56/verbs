'''
Created on Aug 14, 2013

@author: huhe
'''

from main.define import Define
from lib.redhat import RedHat

class NodeCompute(RedHat):
    '''
    classdocs
    '''


    def __init__(self, hostname, username=Define.NODE_DEFAULT_USERNAME, password=Define.NODE_DEFAULT_PASSWORD):
        '''
        Constructor
        '''
        RedHat.__init__(self, hostname, username, password)        

        
        
    
        
        
        