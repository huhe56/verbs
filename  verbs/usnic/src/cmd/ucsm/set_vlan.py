'''
Created on Aug 21, 2013

@author: huhe
'''

from main_ucsm.define import Define
from lib.ucsm import UCSM


if __name__ == '__main__':
    
    ucsm = UCSM(Define.UCSM_HOSTNAME)
    ucsm.scope_top()
    ucsm._ssh.send_expect_prompt("scope eth-uplink")
    for i in range(205, 233):
        if i == 110: continue
        cmd = "create vlan vlan" + str(i) + " " + str(i)
        #print cmd
        ucsm._ssh.send_expect_prompt(cmd)
        ucsm._ssh.send_expect_prompt("exit")
    ucsm._ssh.send_expect_prompt("commit-buffer")

    
