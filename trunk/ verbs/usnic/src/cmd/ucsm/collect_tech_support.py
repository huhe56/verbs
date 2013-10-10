'''
Created on Aug 27, 2013

@author: huhe
'''

from main.define import Define
from lib.util import Util
from lib.ucsm import UCSM
from lib.node_compute import NodeCompute


if __name__ == '__main__':
    
    
    ucsm = UCSM(Define.UCSM_HOSTNAME);
    ssh = ucsm.get_ssh()
    
    cmd1 = "show tech-support ucsm detail"
    cmd2 = "show tech-support chassis 1 all detail"
    cmd3 = "show tech-support chassis 4 all detail"
    cmd4 = "show tech-support fex 2 detail"
    cmd5 = "show tech-support fex 3 detail"
    cmd6 = "show tech-support server 1 detail"
    
    for cmd in [cmd1, cmd2]:
        Util.collect_tech_support(ssh, cmd)
    
    '''
    Util.collect_ucsm_tech_support(ssh)
    Util.collect_chassis_tech_support(ssh)
    '''
    
    '''
    compute_node = NodeCompute("node02", Define.NODE_USERNAME_ROOT, Define.NODE_DEFAULT_PASSWORD)
    ssh = compute_node.get_ssh()
    Util.collect_usnic_tech_support(ssh) 
    '''
    
    ssh.exit()
    