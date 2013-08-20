'''
Created on Aug 20, 2013

@author: huhe
'''

class Utils(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    @staticmethod
    def read_file(filename):
        fh =  open(filename, 'r')
        content = fh.readlines()
        fh.close
        content = [line.replace("\n", "") for line in content]
        return content


    @staticmethod
    def write_file(filename, content): 
        fh = open(filename, 'w')
        fh.write(content)
        fh.close
    
    
    @staticmethod
    def set_prefix_zero_string(index, length):
        return str(index).zfill(length)
    
