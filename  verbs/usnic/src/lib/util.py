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
        ret_code = ssh.expect(["shell_status=0", "shell_status=1", pexpect.TIMEOUT])
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
    def probe_send_expect(ssh, cmd, expect, interval, probe_max_count):
        try_count = 1
        while try_count <= probe_max_count:
            time.sleep(interval)
            Util._logger.info("probe times: " + str(try_count))
            ssh.send(cmd)
            ret = ssh.expect([pexpect.TIMEOUT, expect], 10)
            if ret == 1:
                Util._logger.info("found pattern " + expect)
                return True
            else:
                try_count = try_count + 1
            
        Util._logger.error("pattern " + expect + " not found after trying " + str(probe_max_count) + " times")
        return False
    
        
    '''
    cmd
    expect
    timeout
    return:     save the matched string for future step to use
    for:        loop the cmd multiple times
    probe:      probe until pattern is expected
    '''    
    @staticmethod
    def run_step_list(ssh, file_json_step):
        json_file = open(file_json_step)    
        step_list = json.load(json_file)
        json_file.close()
        
        ret = None
        for step in step_list:
            step_cmd = step["cmd"]
            step_for = None
            if "for" in step.keys(): step_for = step["for"]
            
            if step_for:
                for i in range(0, step_for):
                    step_cmd_i = step_cmd.replace("[$i]", "[" + str(i) + "]")
                    Util._logger.debug("")
                    Util._logger.debug(step_cmd_i)
                    Util._logger.debug("")
                    Util.run_step(ssh, step_cmd_i, step, ret)
                    time.sleep(5)
            else:
                Util._logger.debug(step_cmd)
                ret = Util.run_step(ssh, step_cmd, step, ret)
                    
                    
    @staticmethod
    def run_step(ssh, step_cmd, step, ret=None):
        step_probe  = None
        step_expect = None
        if "probe"  in step.keys(): step_probe  = step["probe"]
        if "expect" in step.keys(): step_expect = step["expect"]
        
        cmd_str = None
        cmd_item_list = re.compile("\s+").split(step_cmd)
        for cmd_item in cmd_item_list:
            if cmd_item.startswith("$"):
                cmd_item = eval(cmd_item[1:])
            if cmd_str : cmd_str = cmd_str + " " + cmd_item
            else: cmd_str = cmd_item
        Util._logger.info(cmd_str)
        
        if step_probe:
            while True:
                time.sleep(step_probe)
                return_code = Util.run_cmd(ssh, cmd_str, [pexpect.TIMEOUT, step_expect], step)
                if return_code != 0:
                    break
        else:
            ret = Util.run_cmd(ssh, cmd_str, step_expect, step)
            Util._logger.debug(ret)
            return ret
    
    
    @staticmethod
    def run_cmd(ssh, cmd, expect_list, step):
        step_timeout = None
        step_return = None
        if "timeout" in step.keys(): step_timeout = int(step["timeout"])
        if "return"  in step.keys(): step_return  = step["return"]
        
        if expect_list:
            Util._logger.debug(expect_list)
            ssh.send(cmd)
            if step_timeout:
                if step_return:
                    ssh.expect(expect_list, step_timeout)
                    return ssh.get_match_object().group()
                else:
                    return ssh.expect(expect_list, step_timeout)
            else:
                if step_return:
                    ssh.expect(expect_list)
                    return ssh.get_match_object().group()
                else:
                    return ssh.expect(expect_list)
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
            if line == "": continue
            if line.startswith("#"): continue
            if pattern1.search(line):
                node_list_1 = pattern1.split(line)
                node_list = node_list + node_list_1
            elif pattern2.search(line):
                m = pattern2.search(line)
                rangex = m.group("range")
                hostname_prefix = line.replace("[" + rangex + "]", "")
                range_item_list = pattern3.split(rangex)
                for i in range(int(range_item_list[0]), int(range_item_list[1])+1):
                    hostname = hostname_prefix + str(i).zfill(2)
                    node_list.append(hostname)
            else:
                node_list.append(line)
        return sorted(node_list)


    @staticmethod
    def collect_ucsm_tech_support(ssh):
        file_json_step = Define.PATH_USNIC_JSON_UCSM + "collect_ucsm_tech_support.json"
        Util.run_step_list(ssh, file_json_step)
        
        
    @staticmethod
    def collect_chassis_tech_support(ssh):
        file_json_step = Define.PATH_USNIC_JSON_UCSM + "collect_chassis_tech_support.json"
        Util.run_step_list(ssh, file_json_step)
        
        
    @staticmethod
    def collect_usnic_tech_support(ssh):
        file_json_step = Define.PATH_USNIC_JSON_LINUX + "collect_usnic_tech_support.json"
        Util.run_step_list(ssh, file_json_step)
        
        
    @staticmethod
    def collect_tech_support(ssh, cmd):
        ssh.send_expect_prompt("top")
        ssh.send_expect_prompt("connect local-mgmt")
        ssh.send(cmd)
        ssh.expect("workspace:.+tar", 600)
        match_str = ssh.get_match_object().group()
        Util._logger.debug("match string: " + match_str)
        cmd_str = "copy " + match_str + " " + Define.URL_UCSM_CDETS_TECH_SUPPORT
        ssh.send(cmd_str)
        ssh.expect("password")
        ssh.send(Define.CDEST_HUHE_PASSWORD)
        
    
        
    