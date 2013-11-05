'''
Created on Oct 31, 2013

@author: huhe
'''

import time
import pexpect

from main.define import Define
from lib.logger import MyLogger
from utils.utils import Utils


class TestBase(object):
    '''
    classdocs
    '''


    def init(self, ssh):
        self._logger = MyLogger.getLogger(self.__class__.__name__)
        self._ssh = ssh
    
    def send(self, cmd):
        self._ssh.send(cmd)
        
    
    def expect(self, expected, timeout=10):
        return self._ssh.expect([expected, pexpect.TIMEOUT], timeout)
    
    
    def check_shell_status(self, positive=True):
        time.sleep(5)
        self._ssh.send("echo status=$?")
        status_str = None
        if positive:
            status_str = "status=0"
        else:
            status_str = "status=1"
        ret = self._ssh.expect(status_str, 10)
        self.assertEqual(ret, 0)
        
        
    def init_test(self, test_name):
        message = "\n\n====================== " + test_name + " =====================\n\n"
        self._logger.info(message)
        Utils.write_file(Define.PATH_USNIC_LOG_FILE_ALL, message)
        
        
        