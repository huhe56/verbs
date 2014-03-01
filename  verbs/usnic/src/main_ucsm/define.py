'''
Created on Aug 15, 2013

@author: huhe
'''

PEXPECT_OUTPUT_STDOUT   = True

class Define(object):
    '''
    classdocs
    '''
    
    UCSM_BUNDLE_LATEST_BUILD_NUMBER     = 333
    UCSM_BUNDLE_LATEST_BUILD_REVISION   = "131023-180144-rev148217-333"
    
    NODE_DEFAULT_USERNAME   = 'huhe'
    NODE_USERNAME_ROOT      = 'root'
    NODE_DEFAULT_PASSWORD   = 'nbv12345'
    
    PATH_DOWNLOADS          = "/home/huhe/Downloads/"
    
    PATH_USNIC_ROOT         = "/home/huhe/workspace/usnic/"
    
    PATH_USNIC_SRC          = PATH_USNIC_ROOT + "src/"
    PATH_USNIC_JSON         = PATH_USNIC_SRC + "json/"
    PATH_USNIC_JSON_LINUX   = PATH_USNIC_JSON + "linux/"
    PATH_USNIC_JSON_UCSM    = PATH_USNIC_JSON + "ucsm/"
    
    PATH_USNIC_CONFIG       = PATH_USNIC_ROOT + "config/"
    PATH_USNIC_LOG          = PATH_USNIC_ROOT + "log/"
    PATH_USNIC_LOG_FILE     = PATH_USNIC_LOG + "pexpect.log"
    PATH_USNIC_LOG_FILE_ALL = PATH_USNIC_LOG + "all.log"

    PATH_TEST_CASE      = PATH_USNIC_SRC + "test_case/"
    PATH_TEST_CASE_UCSM = PATH_TEST_CASE + "ucsm/"
    
    DEVICE_DEFAULT_USERNAME = 'admin'
    DEVICE_DEFAULT_PASSWORD = 'passsword'

    CIMC_DEFAULT_USERNAME   = 'admin'
    CIMC_DEFAULT_PASSWORD   = 'password'
    
    UCSM_DEFAULT_USERNAME   = 'admin'
    UCSM_DEFAULT_PASSWORD   = 'Nbv12345'

    TIMEOUT_SSH         = 10
    PATTERN_SSH_NEW_KEY = '(?i)are you sure you want to continue connecting'
    PATTERN_PASSWORD    = '(?i)password'
    PATTERN_PROMPT      = '[#$]'
    
    TIMEOUT_COMMIT = 60
    
    PATTERN_NEW_LINE    = "\r\n"

    NODE_HEAD_NAME  = "10.193.212.18"
    UCSM_HOSTNAME   = "10.193.212.1"
    
    UCSM_BLADE_SERVER_LIST  = { 1: {
                                    #1: "Blade1_node01", 
                                    2: "Blade2_node02",
                                    #3: "Blade3_node03",
                                    #4: "Blade4_node04", 
                                    #5: "Blade5_node05", 
                                    #7: "Blade7_node06",
                                    }
                               }
    UCSM_RACK_SERVER_LIST   = {
                               #1: "Rack-01_node07", 
                               #2: "Rack-02_node08", 
                               #3: "Rack-03_node09", 
                               #4: "Rack-04_node10",
                               #5: "Rack-05_node11",
                               6: "Rack-06_node12",
                               }
    
    
    URL_IMAGE_BUILD_ROOT = "http://savbu-swucs-bld3.cisco.com/mainline-builds/"
    URL_IMAGE_LATEST_BUILD_ROOT = URL_IMAGE_BUILD_ROOT + UCSM_BUNDLE_LATEST_BUILD_REVISION + "/Images." + str(UCSM_BUNDLE_LATEST_BUILD_NUMBER) + "/"
    IMAGE_LIST = [
                  "ucs-k9-bundle-infra.2.2.0." + str(UCSM_BUNDLE_LATEST_BUILD_NUMBER) + ".A.gbin",
                  "ucs-k9-bundle-b-series.2.2.0." + str(UCSM_BUNDLE_LATEST_BUILD_NUMBER) + ".B.bin",
                 "ucs-k9-bundle-c-series.2.2.0." + str(UCSM_BUNDLE_LATEST_BUILD_NUMBER) + ".C.bin"
                  ]
    URL_IMAGE_LIST = [URL_IMAGE_LATEST_BUILD_ROOT + image for image in IMAGE_LIST]
    
    CMD_SCP_IMAGE_ROOT = "scp://" + NODE_DEFAULT_USERNAME + "@" + NODE_HEAD_NAME + "/" + PATH_DOWNLOADS + "/"
    CMD_SCP_IMAGE_LIST = [CMD_SCP_IMAGE_ROOT + image for image in IMAGE_LIST ]
    
    CDEST_HUHE_PASSWORD = "he100he"
    URL_NODE_CDETS_TECH_SUPPORT = "huhe@10.193.175.2:/net/savbu-da01/qa/cdets/huhe/temp-tech-support"
    URL_UCSM_CDETS_TECH_SUPPORT = "scp://huhe@10.193.175.2/net/savbu-da01/qa/cdets/huhe/temp-tech-support"
    
    
    SERVER_TYPE_BLADE   = "blade",
    SERVER_TYPE_RACK    = "rack",
    
    MAC_PREFIX  = "00:25:B5"
    
    VNIC_POLICY_TYPE_QOS                = "qos-policy"
    VNIC_POLICY_TYPE_QOS_LABEL          = "qos"
    VNIC_POLICY_NAME_QOS_BEST_EFFORT    = "BestEffort-1500"
    VNIC_POLICY_NAME_QOS_PLATINUM       = "Platinum-9216"
    
    VNIC_MTU        = "mtu"
    VNIC_MTU_LABEL  = "mtu"
    
    HOST_DRIVER_1   = "node101"
    HOST_DRIVER_2   = "node103"
    
    MPI_HOST        = "--host"
    MPI_NP          = "-np"
    MPI_MCA         = "--mca btl usnic,sm,self"
    MPI_PATH        = "/home/huhe/ompi-tests/imb/src/IMB-MPI1"
    
    MPI_CMD_PINGPOND    = "pingpong"
    
    
    
    
    
    