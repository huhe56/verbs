'''
Created on Aug 14, 2013

@author: huhe
'''


class Base(object):
    '''
    classdocs
    '''


    def __init__(self, ssh):
        '''
        Constructor
        '''
        '''
        cimc: ssh session to rack server cimc
        ucsm: ssh session to ucsm
        '''
        self._ssh = ssh
        