'''
Created on Aug 13, 2013

@author: huhe
'''

import re 

from main.define import Define
from lib.ssh import SSH
from lib.fw import FW


class CIMC(FW):
    '''
    classdocs
    '''


    def __init__(self, hostname, username=Define.CIMC_DEFAULT_USERNAME, password=Define.CIMC_DEFAULT_PASSWORD):
        '''
        Constructor
        '''
        self._hostname = hostname
        self._username = username
        self._password = password
        FW.__init__(self, SSH(hostname, username, password))        
   
   
    def show_cimc_detail(self):
        self.scope_top()
        self._ssh.send_expect_prompt("show cimc detail")
       
        
    def scope_adapter_from_top(self, adapter_index):
        self.scope_top()
        self.scope_chassis()
        self.scope_adapter(adapter_index)
        
        
    def get_adapter_index_list_from_top(self):
        self.scope_chassis_from_top()
        return self.get_adapter_index_list()
    
    
    def show_adapter_brief(self):
        self._ssh.send_expect_prompt("show adapter")
        
    
    def get_adapter_index_list(self):
        self.show_adapter_brief()
        output = self.get_ssh().get_output()
        lines = output.split(Define.PATTERN_NEW_LINE)
        ret = []
        for line in lines:
            items = re.compile("\s+").split(line)
            if items[1] == Define.CIMC_ADAPTER_UCS and items[2] == Define.CIMC_ADAPTER_VIC and items[3] in Define.CIMC_ADAPTER_SUPPORTED_LIST:
                ret.append(int(items[0]))
        return sorted(ret) 
    
    
    ''' usnic '''
        
    def scope_usnic(self):
        self._ssh.send_expect_prompt("scope usnic-config 0")
        

    def scope_usnic_from_top(self, adapter_index, host_eth_if):
        self.scope_host_eth_if_from_top(adapter_index, host_eth_if)
        self.scope_usnic()
        
    
    def create_usnic(self, count):
        self._ssh.send_expect_prompt("create usnic-config 0")
        self.set_usnic_count(count)
        self.commit()
        
        
    def create_usnic_from_top(self, adapter_index, host_eth_if, count):
        self.scope_host_eth_if_from_top(adapter_index, host_eth_if)
        self.create_usnic_at_host_eth_if(count)
            
            
    def create_usnic_at_host_eth_if(self, count):
        if not self.is_usnic_created():
            self.create_usnic(count)
        else:
            #self._logger.info("usnic already exists at adapter " + str(adapter_index) + ", " + host_eth_if)
            self.scope_usnic()
            self.set_usnic_count(count)
        
        
    def delete_usnic(self, host_eth_if):
        self.set_usnic_count(0)
        
        
    def delete_usnic_from_top(self, adapter_index, host_eth_if):
        self.scope_host_eth_if_from_top(adapter_index, host_eth_if)
        if self.is_usnic_created():
            self.scope_usnic()
            self.set_usnic_count(0)
        else:
            self._logger.info("usnic not exist at adapter " + str(adapter_index) + ", " + host_eth_if)
        
        
    def show_usnic_detail(self):
        self._ssh.send_expect_prompt("show detail")
        
        
    def show_usnic_brief(self):
        self._ssh.send_expect_prompt("show")
        
        
    def show_usnic_brief_at_host_eth_if(self):
        self._ssh.send_expect_prompt("show usnic-config")
        
        
    def set_usnic_count(self, count):
        self._ssh.send_expect_prompt("set usnic-count " + str(count))
        self.commit()
        
        
    def get_usnic_count(self):
        self.show_usnic_brief()
        output = self._ssh.get_output()
        lines = output.split(Define.PATTERN_NEW_LINE)
        if len(lines) < 3:
            return 0
        else:
            items = re.compile("\s+").split(lines[3])
            return int(items[1])
    
    def get_usnic_count_at_host_eth_if(self):
        self.show_usnic_brief_at_host_eth_if()
        output = self._ssh.get_output()#NODE_HOST_IP_2  = 'bcnode20'
    #NODE_CIMC_IP_1  = '10.193.212.
        lines = output.split(Define.PATTERN_NEW_LINE)
        if len(lines) < 3:
            return 0
        else:
            items = re.compile("\s+").split(lines[3])
            return int(items[1])
    
    
    def is_usnic_created(self):
        usnic_count = self.get_usnic_count_at_host_eth_if()
        if usnic_count == 0:
            return False
        else:
            return True
        
    def is_usnic_created_from_top(self, adapter_index, host_eth_if):
        self.scope_host_eth_if_from_top(adapter_index, host_eth_if)
        return self.is_usnic_created()
        
    
    ''' host eth if '''
        
    def scope_host_eth_if_from_top(self, adapter_index, host_eth_if):
        self.scope_adapter_from_top(adapter_index)
        self.scope_host_eth_if(host_eth_if)
        
        
    def show_host_eth_if_brief(self):
        self._ssh.send_expect_prompt("show host-eth-if")
    
    
    def get_host_eth_if_list(self):
        self.show_host_eth_if_brief()
        output = self.get_ssh().get_output()
        lines = output.split(Define.PATTERN_NEW_LINE)
        ret = []
        for line in lines:
            items = re.compile("\s+").split(line)
            if items[0].startswith(Define.CIMC_HOST_ETH_IF):
                ret.append(items[0])
        return ret 
    
    
    def delete_host_eth_if(self, host_eth_if):
        if host_eth_if not in Define.CIMC_DEFAULT_ETH_IF_LIST:
            self._ssh.send_expect_prompt("delete host-eth-if " + host_eth_if)
            self.commit()
        else:
            #self._logger.info(host_eth_if + " is default interface, can not be deleted")
            pass
        
        
    def delete_host_eth_if_from_top(self, adapter_index, host_eth_if):
        self.scope_adapter_from_top(adapter_index)
        self.delete_host_eth_if(host_eth_if)
        
        
    def create_host_eth_if_from_top(self, cimc, adapter_index, host_eth_if_dictionary):
        for host_eth_if, host_eth_if_setting in sorted(host_eth_if_dictionary.iteritems()):
            if host_eth_if not in Define.CIMC_DEFAULT_ETH_IF_LIST:
                cimc.scope_adapter_from_top(adapter_index)
                uplink_index = host_eth_if_setting["uplink"]
                vlan = host_eth_if_setting["vlan"]
                vlan_mode = host_eth_if_setting["vlan-mode"]
                self._ssh.send_expect_prompt("create host-eth-if " + host_eth_if)
                self._ssh.send_expect_prompt("set uplink " + str(uplink_index))
                self._ssh.send_expect_prompt("set vlan-mode " + vlan_mode)
                self._ssh.send_expect_prompt("set vlan " + str(vlan))
                self.commit()
            else:
                self._logger.info(host_eth_if + " is default interface, can not be created")
            
        
    def delete_all_host_eth_if_from_top(self, adapter_index):
        self.scope_adapter_from_top(adapter_index)
        self.delete_all_host_eth_if()
        
        
    def delete_all_host_eth_if(self):
        host_eth_if_list = self.get_host_eth_if_list()
        for host_eth_if in host_eth_if_list:
            self.delete_host_eth_if(host_eth_if)
        host_eth_if_list = self.get_host_eth_if_list()
        if host_eth_if_list != Define.CIMC_DEFAULT_ETH_IF_LIST:
            #self._logger.error("host eth if other than eth0 and e#NODE_HOST_IP_2  = 'bcnode20'
    #NODE_CIMC_IP_1  = '10.193.212.th1 is not deleted")
            return False
        else:
            #self._logger.info("non default host eth if have been deleted")
            return True
            
    
    ''' misc '''
        
    def set_property(self, key, value):
        self._ssh.send_expect_prompt("set " + key + " " + str(value))
        
    
    def show_detail(self):
        self._ssh.send_expect_prompt("show detail")
        
        
    def power_cycle(self):
        self.scope_chassis_from_top()
        self._ssh.send("power cycle")
        self._ssh.expect('\[y\|N\]')
        self._ssh.send_expect_prompt("y")
        
        
    ''' bios '''
    def set_bios_advanced(self, name, value):
        self._ssh.send_expect_prompt("scope bios")
        self._ssh.send_expect_prompt("scope advanced")
        self._ssh.send_expect_prompt("set " + name + " " + value)
        self._ssh.send("commit")
        self._ssh.expect("\[y\|N\]", Define.TIMEOUT_COMMIT)
        self._ssh.send_expect_prompt("y")
        
        
    def show_storage_adapter_detail(self):
        self.scope_chassis_from_top()
        self._ssh.send_expect_prompt("show storageadapter detail")
        
    
