'''
Created on Aug 8, 2013

@author: huhe
'''

import pexpect, sys, re 

from main.define import Define
from lib.logger import MyLogger

class SSH(object):
    '''
    classdocs
    '''
        

    def __init__(self, hostname, username, password):
        self._logger = MyLogger.getLogger(self.__class__.__name__)
        self._session = self.login(hostname, username, password)
        self._pattern_prompt = Define.PATTERN_PROMPT
        

    def login(self, hostname, username, password):        
        cmd = 'ssh ' + username + '@' + hostname
        self._logger.debug(cmd)
        _session = pexpect.spawn(cmd, timeout=Define.TIMEOUT_SSH)
        if Define.PEXPECT_OUTPUT_STDOUT:
            _session.logfile_read = sys.stdout
        else:
            _session.logfile_read = file(Define.PATH_USNIC_LOG_FILE, "w")
        ret = _session.expect([pexpect.TIMEOUT, pexpect.EOF, Define.PATTERN_SSH_NEW_KEY, Define.PATTERN_PROMPT, Define.PATTERN_PASSWORD])
        if ret == 0:
            self._logger.error('timeout when ssh to ' + hostname)
            return None
        elif ret == 1:
            self._logger.error('end of file when ssh to ' + hostname)
            return None
        elif ret == 2:
            _session.sendline('yes')
            _session.expect(Define.PATTERN_PASSWORD)
            _session.sendline(password)
            ret = _session.expect([pexpect.TIMEOUT, Define.PATTERN_PROMPT])
            if ret == 0:
                self._logger.error("timeout after sending password")
                return None
        elif ret == 3:
            pass
        elif ret == 4:
            _session.sendline(password)
            ret = _session.expect([pexpect.TIMEOUT, Define.PATTERN_PROMPT])
            if ret == 0:
                self._logger.error("timeout after sending password")
                return None
        return _session
    
    
    def get_session(self):
        return self._session
    
    
    def is_login_ok(self):
        if self._session: 
            return True
        else:
            return False
    

    def set_prompt(self, prompt):
        self._pattern_prompt = prompt
        
        
    def send(self, cmd):
        self._session.sendline(cmd)
        
    
    def expect(self, pattern, timeout=None):
        return self._session.expect(pattern, timeout)
        
        
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
    
    
    
        
        
            