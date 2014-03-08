'''
Created on Feb 27, 2014

@author: huhe
'''

import json
import time, traceback

from main_ucsm import define
from main_ucsm.define import Define
from main_ucsm.define_mpi import DefineMpi
from lib.logger import MyLogger
from lib.util import Util
from lib.ucsm_server import UcsmServer
from lib.node_compute import NodeCompute


if __name__ == '__main__':
    define.PEXPECT_OUTPUT_STDOUT = False
    
    log = MyLogger.getLogger("create_run_mpi")
    
    path_vnic_default_json_file     = Define.PATH_TEST_CASE_UCSM + "vnic_default.json"
    path_create_run_mpi_json_file   = Define.PATH_TEST_CASE_UCSM + "create_run_mpi_test.json"
    
    vnic_default_data = json.load(open(path_vnic_default_json_file))
    test_case_data = json.load(open(path_create_run_mpi_json_file))
    
    #log.debug(vnic_default_data)
    #log.debug(test_case_data)
    
    ucsm_server_list = UcsmServer.init_ucsm_server(Define.UCSM_HOSTNAME)
    test_result_summary = []
    for test_case in test_case_data:
        test_case_name = None
        test_case_type = None
        try:
            log.info("")
            log.info("")
            test_case_name = test_case['name']
            test_case_type = test_case['type'] if 'type' in test_case else DefineMpi.TEST_TYPE_POSITIVE
            node_count = test_case['node count']
            node_list = test_case['nodes']
            np = test_case['np'] if 'np' in test_case else None
            mpi = test_case['mpi'] if 'mpi' in test_case else DefineMpi.MPI_CMD_DEFAULT
            message_list = test_case['message'] if 'message' in test_case else [0]
            
            log.info("="*25 + " " + test_case_type.title() + ": " + test_case_name + " " + "="*25)
            
            node_list = Util.populate_node_list(node_count, node_list)
            #pprint(node_list)
            
            ret = True
            if len(node_list) <= len(ucsm_server_list):
                i = 0
                for node in node_list:
                    ucsm_server = ucsm_server_list[i]
                    ucsm_server.get_all_vnics_attributes()
                    ucsm_server.delete_all_vnics()
                    ucsm_server.configure(node, vnic_default_data)
                    i += 1
            
            if np:
                if Define.CONFIG:
                    log.info("wait for nodes to reboot ...")
                    time.sleep(420)
                
                i = 0
                host_list = []
                for node in node_list:
                    ucsm_server = ucsm_server_list[i]
                    log.info("waiting for " + ucsm_server._host_name + " to boot up ...")
                    host = NodeCompute.wait_for_node_to_boot_up(ucsm_server._host_name)
                    host.set_ucsm_server_vnic_dict(ucsm_server.get_vnic_dict())
                    host_list.append(host)
                    i += 1
                    
                for host in host_list:
                    host.check_usnic_configured_vf()
                    
                i = 0
                min_total_cpu_core_count = 9999999
                for host in host_list:
                    ucsm_server = ucsm_server_list[i]
                    count = ucsm_server.get_total_cpu_core_count()
                    host.set_total_cpu_core_count(count)
                    if count < min_total_cpu_core_count:
                        min_total_cpu_core_count = count
                    i += 1
                    
                for host in host_list:
                    host.set_min_total_cpu_core_count(min_total_cpu_core_count)
                    
                param_dictionary = {
                                DefineMpi.MPI_PARAM_CMD: mpi,
                                DefineMpi.MPI_PARAM_NP: np,
                                DefineMpi.MPI_PARAM_HOST_LIST: host_list,
                                DefineMpi.MPI_PARAM_MSG: message_list,
                                }
                ret = host_list[0].run_mpi(param_dictionary, test_case_type)
                
            if ret:
                log.info("")
                log.info("-"*25 + ">>> " + test_case_type.title() + " Test Case Passed: " + test_case_name)
                test_case_result = {}
                test_case_result['name'] = test_case_name
                test_case_result['result'] = ret
                test_case_result['type'] = test_case_type
                test_result_summary.append(test_case_result)
            else:
                raise Exception("failed to run mpi")
                #break
        except Exception, e:
            log.info("")
            log.info("*"*25 + ">>> " + test_case_type.title() + " Test Case Failed: " + test_case_name)
            traceback.print_exc()
            test_case_result = {}
            test_case_result['name'] = test_case_name
            test_case_result['result'] = False
            test_case_result['type'] = test_case_type
            test_result_summary.append(test_case_result)
            #break
    
    time.sleep(10)
    log.info("")
    log.info("")
    log.info("="*25 + " Test Result Summary " + "="*25)
    log.info("")
    for test_case_result in test_result_summary:
        result = "Passed" if test_case_result["result"] else "Failed"
        log.info(result + ", " + test_case_result["type"] + ", " + test_case_result['name'])
        
        