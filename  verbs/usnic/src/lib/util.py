'''
Created on Aug 8, 2013

@author: huhe
'''

import re
import time
import simplejson as json
import pexpect

# Define is used, don't remove
from main.define import Define
from lib.logger import MyLogger
from utils.utils import Utils


class Util(object):
    '''
    classdocs
    '''
    _logger = MyLogger.getLogger("Util")


    def __init__(self):
        '''
        Constructor
        '''


    @staticmethod
    def ping(ssh, ip, count):
        ssh.send_expect_prompt("ping -c " + str(count) + " " + ip)
        return Util.check_shell_status(ssh)
        
        
    @staticmethod
    def check_shell_status(ssh):
        ssh.send("echo shell_status=$?")
        ret_code = ssh.expect(["shell_status=0", "shell_status=1"])
        if ret_code == 0: 
            return True
        else:
            return False
        
    
    @staticmethod
    def find_pattern_list(pattern, string):
        print pattern
        m = re.findall(pattern, string)
        print m
        
        
    @staticmethod
    def run_step_list(ssh, file_json_step):
        json_file = open(file_json_step)    
        step_list = json.load(json_file)
        json_file.close()
        
        for step in step_list:
            step_cmd = step["cmd"]
            step_for = None
            if "for" in step.keys(): step_for = step["for"]
            
            if step_for:
                for i in range(0, step_for):
                    step_cmd_i = step_cmd.replace("[$i]", "[" + str(i) + "]")
                    Util._logger.debug(step_cmd_i)
                    Util.run_step(ssh, step_cmd_i, step)
            else:
                Util._logger.debug(step_cmd)
                Util.run_step(ssh, step_cmd, step)
                    
                    
    @staticmethod
    def run_step(ssh, step_cmd, step):
        step_probe  = None
        step_expect = None
        if "probe"  in step.keys(): step_probe  = step["probe"]
        if "expect" in step.keys(): step_expect = step["expect"]
        
        cmd_str = ""
        cmd_item_list = re.compile("\s+").split(step_cmd)
        for cmd_item in cmd_item_list:
            if cmd_item.startswith("$"):
                cmd_item = eval(cmd_item[1:])
            cmd_str = cmd_str + " " + cmd_item
        Util._logger.info(cmd_str)
        
        if step_probe:
            while True:
                time.sleep(step_probe)
                return_code = Util.run_cmd(ssh, cmd_str, [pexpect.TIMEOUT, step_expect], step)
                if return_code != 0:
                    break
        else:
            Util.run_cmd(ssh, cmd_str, step_expect, step)
    
    
    @staticmethod
    def run_cmd(ssh, cmd, expect_list, step):
        step_timeout = None
        if "timeout" in step.keys(): step_timeout = step["timeout"]
        
        if expect_list:
            ssh.send(cmd)
            if step_timeout:
                return ssh.expect(cmd, expect_list, step_timeout)
            else:
                return ssh.expect(cmd, expect_list)
        else:
            if step_timeout:
                return ssh.send_expect_prompt(cmd, step_timeout)
            else:
                return ssh.send_expect_prompt(cmd)
        
        
     
    @staticmethod
    def get_node_name_list(path_config_file):
        pattern1 = re.compile("\s*\,\s*")
        pattern2 = re.compile("\[(?P<range>[0-9\-]+)\]")
        pattern3 = re.compile(r"-")
        node_list = []
        line_list = Utils.read_file(path_config_file)
        for line in line_list:
            line.strip()
            if line.startswith("#"): continue
            if pattern1.search(line):
                node_list_1 = pattern1.split(line)
                node_list = node_list + node_list_1
            elif pattern2.search(line):
                m = pattern2.search(line)
                rangex = m.group("range")
                hostname_prefix = line.replace("[" + rangex + "]", "")
                range_item_list = pattern3.split(rangex)
                for i in range(int(range_item_list[0]), int(range_item_list[1])):
                    hostname = hostname_prefix + str(i).zfill(2)
                    node_list.append(hostname)
            else:
                node_list.append(line)
        return sorted(node_list)