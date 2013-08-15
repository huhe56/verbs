'''
Created on Aug 8, 2013

@author: huhe
'''


from lib.ucsm import UCSM
from lib.ucsm_blade import UcsmBlade


if __name__ == '__main__':
    
    ucsm = UCSM("10.193.212.1")
    
    blade = UcsmBlade(ucsm, 1, 1)
    blade.scope_usnic_from_top(1, "2")
    
    
    
    
    