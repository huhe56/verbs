'''
Created on Aug 13, 2013

@author: huhe
'''

import pexpect
from main_ucsm.define import Define
from lib.logger import MyLogger
from lib.ucsm import UCSM
from lib.ucsm_server_vnic import UcsmServerVnic


class UcsmServer():
    '''
    classdocs
    '''


    def __init__(self, ucsm, chassis_index, server_index):
        '''
        Constructor
        '''
        self._logger = MyLogger.getLogger(self.__class__.__name__)
        self._ucsm = ucsm
        self._server_type = Define.SERVER_TYPE_BLADE
        self._chassis_index = chassis_index
        if not chassis_index: self._server_type = Define.SERVER_TYPE_RACK
        self._server_index = server_index
        self._ssh = ucsm.get_ssh()
        
        self._service_profile = None
        self._host_name = None
        self._vnic_dict = None
        self._total_cpu_core_count = None
        
    @staticmethod
    def init_ucsm_server(ucsm_hostname):
        ucsm_server_list = []
        ucsm = UCSM(ucsm_hostname)
        for chassis_index in Define.UCSM_BLADE_SERVER_LIST:
            for server_index, node in Define.UCSM_BLADE_SERVER_LIST[chassis_index].items():
                service_profile = node["service profile"]
                host_name = node["host name"]
                blade_server = UcsmServer(ucsm, chassis_index, server_index)
                blade_server.set_service_profile(service_profile)
                blade_server.set_host_name(host_name)
                ucsm_server_list.append(blade_server)
        for server_index, node in Define.UCSM_RACK_SERVER_LIST.items():
            service_profile = node["service profile"]
            host_name = node["host name"]
            rack_server = UcsmServer(ucsm, None, server_index)
            rack_server.set_service_profile(service_profile)
            rack_server.set_host_name(host_name)
            ucsm_server_list.append(rack_server)
        return ucsm_server_list
    
    
    def configure(self, node_data, vnic_default_data):
        vnics_data = node_data["vnics"]
        for vnic_data in vnics_data:
            vlan = vnic_data['vlan']
            name = "eth-" + str(vlan)
            ucsm_server_vnic = UcsmServerVnic(self, name)
            ucsm_server_vnic.configure(vnic_data, vnic_default_data)
            self._vnic_dict[name] = ucsm_server_vnic
        if Define.CONFIG:
            self.commit()
            self.reboot_from_top()
        return True
    
    
    def check_profile_vnic_status(self, message):
        self.scope_service_profile_from_top()
        match_list = self._ssh.send_match_list("show status detail", message)
        #self._logger.debug(match_list)
        if match_list:
            if len(match_list) == 1:
                return True
        raise Exception("Can not find usnic config message: " + message)
    
    
    def get_total_cpu_core_count(self):
        if not self._total_cpu_core_count:
            self.scope_server_from_top()
            cpu_core_count_list = self._ssh.send_match_list("show cpu", "(?<=CPU\d)(?:\s+\d+)")
            cpu_core_count_list = [int(x) for x in cpu_core_count_list]
            self._total_cpu_core_count = sum(cpu_core_count_list)
            self._logger.debug("total cpu cores: " + str(self._total_cpu_core_count))
        return self._total_cpu_core_count
    
    
    def get_vnic_dict(self):
        return self._vnic_dict
    
    
    def get_mac_address(self, vlan):
        vlan_str = str(vlan)
        if vlan >= 200:
            ''' handle 32 PFs case '''
            vlan_str = hex(vlan).split("x")[1]
        if self._server_type == Define.SERVER_TYPE_BLADE:
            item_chassis = "C" + str(self._chassis_index)
            item_blade   = "B" + str(self._server_index)
            return ":".join([Define.MAC_PREFIX, item_chassis, item_blade, vlan_str.upper()])
        else:
            item_chassis = "CC"
            item_rack    = "%02d" % self._server_index
            return ":".join([Define.MAC_PREFIX, item_chassis, item_rack, vlan_str.upper()])
    
    
    def get_all_vnics_attributes(self):
        self._vnic_dict = UcsmServerVnic.get_all_attributes(self)
        for vnic_name, vnic in self._vnic_dict.items():
            vnic.debug()
    
    
    def delete_all_vnics(self):
        if Define.CONFIG:
            for vnic_name, vnic in self._vnic_dict.items():
                if vnic_name != "eth-1":
                    vnic.delete()
                    del self._vnic_dict[vnic_name]
                
    
    
    def scope_top(self):
        self._ssh.send_expect_prompt("top")
        
    
    def scope_chassis(self, chassis_index=None):
        if chassis_index:
            self._ssh.send_expect_prompt("scope chassis " + str(chassis_index))
        
        
    def scope_server(self, server_index):
        self._ssh.send_expect_prompt("scope server " + str(server_index))
        
        
    def scope_server_from_top(self):
        self.scope_top()
        self.scope_chassis(self._chassis_index)
        self.scope_server(self._server_index)


    def show_cpu_brief(self):
        self.scope_server_from_top()
        self._ssh.send_expect_prompt("show cpu")
        self._logger.debug(self._ssh.get_output())
        
        
    def set_service_profile(self, service_profile):
        self._service_profile = service_profile
        
        
    def set_host_name(self, host_name):
        self._host_name = host_name
        
        
    def scope_service_profile_from_top(self):
        self._ssh.send_expect_prompt("top")
        self._ssh.send_expect_prompt("scope org")
        self._ssh.send_expect_prompt("scope service-profile " + self._service_profile)
        
        
    def scope_vnic_from_top(self, vnic_name):
        self.scope_service_profile_from_top()
        self._ssh.send_expect_prompt("scope vnic " + vnic_name)
        
    
    def show_vnic_brief(self, vnic_name):
        self.scope_vnic_from_top(vnic_name)
        self._ssh.send_expect_prompt("show")
        
        
    def commit(self):
        self._ssh.send_expect_prompt("commit-buffer")
        
        
    '''
    fabric string can be: a, a-b, b, b-a
    '''
    def set_vnic_fabric(self, fabric_string):
        self._ssh.send_expect_prompt("set fabric " + fabric_string)
        self.commit()
        
        
    def power_on_from_top(self):
        self.scope_service_profile_from_top()
        self._ssh.send_expect_prompt("power up")
        self.commit()
        
        
    def power_off_from_top(self):
        self.scope_service_profile_from_top()
        self._ssh.send_expect_prompt("power down")
        self.commit()
        
        
    def reboot_from_top(self):
        self.scope_service_profile_from_top()
        self._ssh.send_expect_prompt("reboot")
        self.commit()
        
    
    def set_bios_policy(self, bios_policy_name):
        self._ssh.send_expect_prompt("set bios-policy " + bios_policy_name)
        self.commit()
        
        
    def set_boot_policy(self, boot_policy_name):
        self._ssh.send_expect_prompt("set boot-policy " + boot_policy_name)
        self.commit()
        
    def show_boot_policy_brief(self):
        self._ssh.send_expect_prompt("show boot-policy")
        
        
    def set_host_fw_policy(self, host_fw_policy_name):
        self._ssh.send_expect_prompt("set host-fw-policy " + host_fw_policy_name)
        self.commit()
        
    def show_host_fw_policy_brief(self):
        self._ssh.send_expect_prompt("show detail | grep host")
        
        
    def set_vnic_adapter_policy(self, vnic_adapter_policy_name):
        self._ssh.send_expect_prompt("set adapter-policy " + vnic_adapter_policy_name)
        self.commit()
        
        
    def create_vnic_usnic_policy(self, vnic_usnic_policy_name):
        self._ssh.send("show usnic-conn-policy-ref detail")
        ret_index = self._ssh.expect([pexpect.TIMEOUT, "USNIC Connection Policy Name: (?P<usnic>[0-9_a-zA-Z]+)"], 5)
        if ret_index == 0:
            self.create_vnic_usnic_policy_directly(vnic_usnic_policy_name)
        elif ret_index == 1:
            match_str = self._ssh.get_match_object().group("usnic")
            if match_str.lower() == vnic_usnic_policy_name.lower():
                self._logger.info("policy name is the same; old: " + match_str + " == new : " + vnic_usnic_policy_name)
            else:
                self._ssh.send_expect_prompt("delete usnic-conn-policy-ref " + match_str)
                self.commit()
                self.create_vnic_usnic_policy_directly(vnic_usnic_policy_name)
                
    def create_vnic_usnic_policy_directly(self, vnic_usnic_policy_name):
        self._ssh.send_expect_prompt("create usnic-conn-policy-ref " + vnic_usnic_policy_name)
        self.commit()
            
    def show_vnic_usnic_policy_brief(self, vnic_name):
        self.scope_vnic_from_top(vnic_name)
        self._ssh.send_expect_prompt("show usnic-conn-policy-ref")
        

    def disassociate_service_profile(self):
        self._ssh.send_expect_prompt("disassociate")
        self.commit()
        
    def associate_service_profile(self):
        server_index = str(self._server_index)
        if self._chassis_index:
            server_index = str(self._chassis_index) + "/" + server_index
        self._ssh.send_expect_prompt("associate server " + server_index)
        self.commit()
        
    
    '''
    generic set vnic policy method
    '''
    def set_vnic_policy(self, vnic_name, vnic_policy_type, vnic_policy_name):
        self.scope_vnic_from_top(vnic_name)
        self._ssh.send_expect_prompt("set " + vnic_policy_type + " " + vnic_policy_name)
        self.commit()
        
    def show_vnic_policy(self, vnic_name, vnic_policy_label):
        self.scope_vnic_from_top(vnic_name)
        self._ssh.send_expect_prompt("show detail | grep -i " + vnic_policy_label)
        
        
    '''
    generic set service profile policy method
    '''
    def set_service_profile_policy(self, policy_type, policy_name):
        self._ssh.send_expect_prompt("set " + policy_type + " " + policy_name)
        self.commit()
        
    def show_service_profile_policy(self, policy_label):
        self._ssh.send_expect_prompt("show detail | grep -i " + policy_label)
        
