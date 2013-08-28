'''
Created on Aug 26, 2013

@author: huhe
'''

import time
import pexpect

from main.define import Define
from lib.ucsm import UCSM


if __name__ == '__main__':
    
    ucsm = UCSM(Define.UCSM_HOSTNAME);
    ssh = ucsm.get_ssh()
    
    for i in range(0, 3):
        ssh.send_expect_prompt("top")
        ssh.send_expect_prompt("scope firmware")
        ssh.send("download image " + Define.CMD_SCP_IMAGE_LIST[i])
        ssh.expect(Define.PATTERN_PASSWORD)
        ssh.send_expect_prompt(Define.NODE_DEFAULT_PASSWORD)
        ssh.send_expect_prompt("scope download-task " + Define.IMAGE_LIST[i])
        
        try_count = 0
        while True:
            time.sleep(60)
            ssh.send("show")
            ret = ssh.expect([pexpect.TIMEOUT, "Downloaded"])
            if ret == 1:
                break
            try_count = try_count + 1
            if try_count == 10:
                print "\nERROR: failed after trying " + str(try_count) + " times"
                break
            else:
                print "\nINFO: have tried for " + str(try_count) + " times" 
            
        
        
        