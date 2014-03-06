'''
Created on Feb 26, 2014

@author: huhe
'''

        
class DefineMpi:
    
    
    HOST_USNIC_ETH_IF_START_INDEX = 2
    
    #NODE_HOST_LIST  = [NODE_HOST_IP_1, NODE_HOST_IP_2]
    #NODE_CIMC_LIST  = [NODE_CIMC_IP_1, NODE_CIMC_IP_2]
    #NODE_NUMBER     = len(NODE_HOST_LIST)
    #NODE_HOST_LIST_DEFAULT = NODE_HOST_LIST
    
    MPI_PARAM_CMD                   = "cmd"
    MPI_PARAM_MSG                   = "message"
    MPI_PARAM_VF_USED_COUNT_LIST    = "vf_used_count_list"
    MPI_PARAM_TIMEOUT               = "timeout"
    MPI_PARAM_HOST_LIST             = "host_list"
    
    MPI_PARAM_HOST      = "--host"
    
    MPI_PARAM_NP        = "-np"
    MPI_NP_DEFAULT      = 32
    
    MPI_PARAM_MCA       = "--mca"
    MPI_MCA_DEFAULT     = "btl usnic,sm,self"
    
    MPI_MCA_INCLUDE_USNIC_PREFIX    = "btl_usnic_include usnic_"
    MPI_MCA_INCLUDE_ETH_PREFIX      = "btl_usnic_include eth"
    
    
    MPI_PATH        = "/home/huhe/ompi-tests/imb/src/IMB-MPI1"
    
    MPI_CMD_PINGPONG    = "pingpong"
    MPI_CMD_SENDRECV    = "Sendrecv"
    MPI_CMD_ALLTOALL    = "Alltoall"
    MPI_CMD_ALL         = "All"
    MPI_CMD_DEFAULT     = MPI_CMD_ALLTOALL
    
    MPI_CMD_TIMEOUT_PINGPONG    = 30
    MPI_CMD_TIMEOUT_ALLTOALL    = 600
    MPI_CMD_TIMEOUT_ALL         = 1800
    
    MPI_MESSAGE_FINISH              = "All processes entering MPI_Finalize"
    MPI_MESSAGE_NOT_ENOUGH_USNIC    = "not enough usNIC"
    MPI_MESSAGE_NOT_ENOUGH_CORE     = "An invalid physical processor ID was returned"
    MPI_MESSAGE_DEFAULT             = MPI_MESSAGE_FINISH
    
    MPI_MESSAGE_ABORT           = "abort"
    MPI_MESSAGE_WARN            = "warn"
    MPI_MESSAGE_ERROR           = "error"
    
    MPI_MESSAGE_DICT = {
                        0: MPI_MESSAGE_FINISH,
                        1: MPI_MESSAGE_NOT_ENOUGH_USNIC,
                        2: MPI_MESSAGE_NOT_ENOUGH_CORE
                        }
    
    
    