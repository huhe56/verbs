'''
Created on Aug 27, 2013

@author: huhe
'''

from main.define import Define
from lib.util import Util
from lib.ucsm import UCSM
from lib.node_compute import NodeCompute


if __name__ == '__main__':
    
    '''
    ucsm = UCSM(Define.UCSM_HOSTNAME);
    ssh = ucsm.get_ssh()
    
    file_tech_support = Util.collect_ucsm_tech_support(ssh)
    print file_tech_support
    '''
    
    compute_node = NodeCompute("node02", Define.NODE_USERNAME_ROOT, Define.NODE_DEFAULT_PASSWORD)
    ssh = compute_node.get_ssh()
    file_tech_support = Util.collect_usnic_tech_support(ssh) 
    print file_tech_support