'''
Created on Aug 8, 2013

@author: huhe
'''

import sys, pexpect

from main.define import Define
from lib.ssh import SSH

if __name__ == '__main__':
    
    myssh = SSH('10.193.212.20', 'root', 'nbv12345')
    myssh.send('ls -l')
    #print myssh._ssh.readlines()
    myssh.expect(Define.PATTERN_PROMPT)
    print "\n\n--------> before: " + myssh._session.before
    myssh.send('pwd')
    #print myssh._ssh.readlines()
    myssh.expect('Define.PATTERN_PROMPT')
    #myssh.expect(pexpect.EOF)
    print "\n\n--------> before: " + myssh._session.before
    #print "\n\buffer: " + myssh._ssh.buffer
    #print "\n\nafter: " + myssh._ssh.after
    myssh.send('exit')
    
    