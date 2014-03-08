'''
Created on Feb 27, 2014

@author: huhe
'''

from main_ucsm.define import Define
from lib.logger import MyLogger


class UcsmServerVnic(object):
    '''
    classdocs
    '''


    def __init__(self, ucsm_server, name):
        '''
        Constructor
        '''
        self._logger = MyLogger.getLogger(self.__class__.__name__)
        
        self._ucsm_server = ucsm_server
        self._attribute_dict = {}
        
        self._name          = name
        self._vlan          = None
        self._vlan_policy   = None
        self._usnic         = None
        self._usnic_policy  = None
        self._fabric        = None
        self._mtu           = None
        self._mac           = None
        self._adapter_policy    = None
        self._qos_policy        = None
        self._usnic_message_index = None
        
        
    @staticmethod
    def get_all_attributes(ucsm_server):
        vnic_dict = {}
        ucsm_server.scope_service_profile_from_top()
        ucsm_server._ssh.send_expect_prompt("show vnic detail")
        output = ucsm_server._ssh.get_output()
        line_list = output.split("\r\n")
        current_vnic = None
        for line in line_list:
            line = line.strip()
            if line.startswith("Name: "):
                key, value = line.split(": ")
                current_vnic = UcsmServerVnic(ucsm_server, value)
                vnic_dict[value] = current_vnic
            elif current_vnic :
                if line.find(":") > 0:
                    item_list = line.split(": ")
                    if len(item_list) == 2:
                        current_vnic.set_attribute(item_list[0], item_list[1])
        return vnic_dict
                    
                    
    def set_attribute(self, key, value):
        self._attribute_dict[key] = value
        
        
    def delete(self):
        if (self._name != "eth-1"):
            self._ucsm_server.scope_service_profile_from_top()
            self._ucsm_server._ssh.send_expect_prompt("delete vnic " + self._name)
            self._ucsm_server._ssh.send_expect_prompt("commit-buffer")
            self._logger.info(self._ucsm_server._service_profile + " " + self._name + " is deleted")
        else:
            self._logger.info(self._ucsm_server._service_profile + " " + self._name + " can't be deleted")
        
        
    def configure(self, vnic_data, vnic_default_data):
        self._vlan = vnic_data['vlan']
        self._vlan_policy = "vlan" + str(self._vlan)
        
        if "fabric" in vnic_data:
            self._fabric = vnic_data['fabric']
        else:
            if (self._vlan/10)%2 == 0:
                self._fabric = 'b'
            else:
                self._fabric = 'a'
            
        if "mtu" in vnic_data:
            self._mtu = vnic_data["mtu"]
        else:
            self._mtu = vnic_default_data["mtu"]
            
        if "mac" in vnic_data:
            self._mac = vnic_data["mac"]
        else:
            self._mac = self._ucsm_server.get_mac_address(self._vlan)
            
        if "adapter policy" in vnic_data:
            self._adapter_policy = vnic_data["adapter policy"]
        else:
            self._adapter_policy = vnic_default_data["adapter policy"]
            
        if "qos policy" in vnic_data:
            self._qos_policy = vnic_data['qos policy']
        else:
            self._qos_policy = vnic_default_data['qos policy']
            
        if "usnic" in vnic_data:
            self._usnic = vnic_data["usnic"]
        else:
            self._usnic = vnic_default_data["usnic"]
        self._usnic_policy = str(self._usnic) + "_usNIC"
        
        if "message" in vnic_data:
            self._usnic_message_index = vnic_data['message']
        else:
            self._usnic_message_index = vnic_default_data['message']
            
        if Define.CONFIG:
            self.create_vnic_from_top()
            self.set_default_net()
            self.set_mac_address()
            self.set_mtu()
            self.set_order()
            self.set_adapter_policy()
            self.set_qos_policy()
            self.create_usnic()
        
    
    def create_vnic_from_top(self):
        self._ucsm_server.scope_service_profile_from_top()
        cmd = "create vnic " + self._name + " eth-if " + self._vlan_policy + " fabric " + self._fabric
        self._ucsm_server._ssh.send_expect_prompt(cmd)
        
        
    def set_order(self):
        order = int(self._vlan/10) + 1
        self._ucsm_server._ssh.send_expect_prompt("set order " + str(order))
        
        
    def create_vlan(self):
        self._ucsm_server._ssh.send_expect_prompt("create eth-if " + self._vlan_policy)
        self._ucsm_server._ssh.send_expect_prompt("exit")
        
        
    def set_default_net(self):
        self._ucsm_server._ssh.send_expect_prompt("scope eth-if " + self._vlan_policy)
        self._ucsm_server._ssh.send_expect_prompt("set default-net yes")
        self._ucsm_server._ssh.send_expect_prompt("exit")
        
        
    def create_usnic(self):
        self._ucsm_server._ssh.send_expect_prompt("create usnic-conn-policy-ref " + self._usnic_policy)
        self._ucsm_server.commit()
        self._ucsm_server._ssh.send_expect_prompt("show detail")
        output = self._ucsm_server._ssh.get_output()
        sub_str = "usNIC Connection Policy Name: " + self._usnic_policy
        if sub_str in output:
            self._logger.info("Passed: " + self._ucsm_server._service_profile + ", " + self._name + ", " + self._usnic_policy + " has been created")
            message = Define.USNIC_MESSAGE_DICT[self._usnic_message_index]
            found = self._ucsm_server.check_profile_vnic_status(message)
            if found:
                self._logger.info("Passed: " + self._ucsm_server._service_profile + ", " + self._name + ", found usNIC config message: " + message)
        else:
            self._logger.info("Failed: " + self._ucsm_server._service_profile + ", " + self._name + ", " + self._usnic_policy + " has not been created")
            raise Exception("Failed to create usnic " + self._usnic_policy)
        
        self._ucsm_server._ssh.send_expect_prompt("exit")
        
        
    def set_mac_address(self):
        self._ucsm_server._ssh.send_expect_prompt("set identity dynamic-mac " + self._mac)
        
        
    def set_mtu(self):
        self._ucsm_server._ssh.send_expect_prompt("set mtu " + str(self._mtu))
        
        
    def set_adapter_policy(self):
        self._ucsm_server._ssh.send_expect_prompt("set adapter-policy " + self._adapter_policy)
        
        
    def set_qos_policy(self):
        self._ucsm_server._ssh.send_expect_prompt("set qos-policy " + self._qos_policy)
        
        
    def get_usnic_count(self):
        return self._usnic
    
    
    def get_mac_address(self):
        return self._mac
    
    
    def get_vlan(self):
        return self._vlan
    
    
    def debug(self):
        self._logger.debug("vnic name: " + self._name)
        self._logger.debug(self._attribute_dict)
        
                
        