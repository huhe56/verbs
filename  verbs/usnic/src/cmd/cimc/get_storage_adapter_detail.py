'''
Created on Aug 21, 2013

@author: huhe
'''

from main import define
from main.define import Define
from lib.cimc import CIMC
from lib.util import Util


if __name__ == '__main__':
    
    define.PEXPECT_OUTPUT_STDOUT = True
    
    path_config_file = Define.PATH_USNIC_CONFIG + "cimc.cfg"
    cimc_ip_list = Util.get_node_name_list(path_config_file)
    print cimc_ip_list
    
    for cimc_ip in cimc_ip_list:
        try:
            cimc = CIMC(cimc_ip)
            cimc.show_storage_adapter_detail()
            cimc.exit_ssh()
        except:
            pass
    