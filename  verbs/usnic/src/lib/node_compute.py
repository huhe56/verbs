'''
Created on Aug 14, 2013

@author: huhe
'''

from main.define import Define, DefineMpi
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

        
    def get_usnic_configured_count_list(self):
        usnic_count_list = []
        ret_list = self._ssh.send_match_list("/opt/cisco/usnic/bin/usnic_status", "(?:\d+)\sVFs")
        ret_list = [int(x.replace(" VFs", "")) for x in ret_list]
        for index, element in enumerate(ret_list):
            if index % 2 == 0:
                usnic_count_list.append(element)
        return usnic_count_list
    
    def get_usnic_used_count_list(self):
        usnic_count_list = []
        ret_list = self._ssh.send_match_list("/opt/cisco/usnic/bin/usnic_status", "(?:\d+)\sVFs")
        ret_list = [int(x.replace(" VFs", "")) for x in ret_list]
        for index, element in enumerate(ret_list):
            if index % 2 == 1:
                usnic_count_list.append(element)
        return usnic_count_list
    
    
    def run_mpi(self, mpi_cmd, timeout):
        self._logger.info(mpi_cmd)
        self._ssh.send(mpi_cmd)
        ret = self._ssh.expect(DefineMpi.MPI_MESSAGE_FINISH + ".*" + Define.PATTERN_PROMPT, timeout=30)
        return ret
    
        
        
        