'''
Created on Aug 20, 2013

@author: huhe
'''

from lib.util import Util
from lib.ssh import SSH


if __name__ == '__main__':
    ssh = SSH("10.193.212.1", "huhe", "Nbv12345")
    if ssh.is_login_ok():
        status = Util.ping(ssh, "10.193.212.1", 2)
        if status:
            print "---------passed"
        else:
            print "+++++++++failed"