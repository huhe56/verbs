'''
Created on Aug 8, 2013

@author: huhe
'''

import sys, pexpect

from main.define import Define
from lib.ssh import SSH

if __name__ == '__main__':
    
    myssh = SSH.login('10.193.212.20', 'root', 'nbv12345')
    myssh.sendline('ls -l')
    #print myssh._ssh.readlines()
    myssh.expect(Define.PATTERN_PROMPT)
    print "\n\n--------> before: " + myssh.before
    myssh.sendline('pwd')
    #print myssh._ssh.readlines()
    myssh.expect('/root')
    #myssh.expect(pexpect.EOF)
    print "\n\n--------> before: " + myssh.before
    #print "\n\buffer: " + myssh._ssh.buffer
    #print "\n\nafter: " + myssh._ssh.after
    myssh.send('exit')
    
    