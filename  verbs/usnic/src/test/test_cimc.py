'''
Created on Aug 8, 2013

@author: huhe
'''


from lib.cimc import CIMC


if __name__ == '__main__':
    
    cimc = CIMC('10.193.212.101')
    
    adapter_index = 1
    host_eth_if = "eth1"
    count = 15
    
    
    cimc.delete_usnic_from_top(adapter_index, host_eth_if)
    
    #ret = cimc.is_usnic_created_from_top(adapter_index, host_eth_if)
    #print ret 
    
    #cimc.create_usnic_from_top(adapter_index, host_eth_if, count)
    #ret = cimc.get_usnic_count()
    #print ret
    
    #cimc.set_usnic_count_from_top(adapter_index, host_eth_if, count)
    
    '''
    cimc.scope_usnic_from_top(7, 'eth0')
    cimc.get_detail()
    #cimc.set_count(16)
    cimc.get_brief()
    #output = cimc.get_output()
    print "\n\ncount: " + cimc.get_count()
    '''
    
    '''
    cimc.scope_adapter_from_top(7)
    cimc.create("eth07002", 16)
    
    cimc.scope_usnic_from_top(7, "eth07002")
    print "\n\ncount: " + cimc.get_count()
    
    cimc.scope_adapter_from_top(7)
    cimc.delete("eth07002")
    
    cimc.exit()
    '''
    
    
    
    
    