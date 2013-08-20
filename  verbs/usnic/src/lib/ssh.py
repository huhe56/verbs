'''
Created on Aug 8, 2013

@author: huhe
'''

import pexpect, sys, re 

from main.define import Define
from lib.logger import MyLogger
from lib.util import Util

class SSH(object):
    '''
    classdocs
    '''
    _logger = MyLogger.getLogger('SSH')
    

    def __init__(self, hostname, username, password):
        self._session = SSH.login(hostname, username, password)
        self._pattern_prompt = Define.PATTERN_PROMPT
        

    @staticmethod
    def login(hostname, username, password):        
        cmd = 'ssh ' + username + '@' + hostname
        SSH._logger.info(cmd)
        _session = pexpect.spawn(cmd, timeout=Define.TIMEOUT_SSH)
        _session.logfile_read = sys.stdout
        ret = _session.expect([pexpect.TIMEOUT, Define.PATTERN_SSH_NEW_KEY, Define.PATTERN_PROMPT, Define.PATTERN_PASSWORD])
        if ret == 0:
            SSH._logger.debug('ERROR: timeout when ssh to ' + hostname)
            raise Exception('ssh timeout')
        elif ret == 1:
            _session.sendline('yes')
            _session.expect(Define.PATTERN_PASSWORD)
            _session.sendline(password)
            _session.expect(Define.PATTERN_PROMPT)
        elif ret == 2:
            pass
        elif ret == 3:
            _session.sendline(password)
            _session.expect(Define.PATTERN_PROMPT)
        return _session
    

    def set_prompt(self, prompt):
        self._pattern_prompt = prompt
        
        
    def send(self, cmd):
        self._session.sendline(cmd)
        
    
    def expect(self, pattern):
        return self._session.expect(pattern)
        
        
    def send_expect_prompt(self, cmd, timeout=None):
        self._session.sendline(cmd)
        if timeout:
            return self._session.expect(self._pattern_prompt, timeout)
        else:
            return self._session.expect(self._pattern_prompt)
        
    
    def send_match_list(self, cmd, pattern, timeout=None):        
        self.send_expect_prompt(cmd)
        output = self.get_output()
        #self._logger.debug(output)
        re_pattern = re.compile(pattern)
        match_list = re_pattern.findall(output)
        #self._logger.debug(match_list)
        return match_list
        
        
    def flush(self):
        self._session.flush()
        
        
    def get_output(self):
        return self._session.before + self._session.after
    
    
    
        
        
            