'''
Created on Aug 20, 2013

@author: huhe
'''

import datetime


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
        fh = open(filename, 'a')
        fh.write(content)
        fh.close
    
    
    @staticmethod
    def append_file(target, source):
        f_target = open(target, "a")
        f_source = open(source, "r")
        f_target.write(f_source.read())
        f_target.close()
        
    
    @staticmethod
    def set_prefix_zero_string(index, length):
        return str(index).zfill(length)
    
    
    @staticmethod
    def get_current_time_string():
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        
        
        
        
        
        
