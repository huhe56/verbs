'''
Created on Aug 20, 2013

@author: huhe
'''

import datetime, os, shutil


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
        
        
    @staticmethod
    def move_all_files(src, dst):
        files = os.listdir(src)
        for file1 in files:
            file1_path = src + file1
            if os.path.isfile(file1_path):
                shutil.move(file1_path, dst)
        
    
    @staticmethod
    def delete_all_files(dst):
        files = os.listdir(dst)
        for file1 in files:
            file1_path = dst + file1
            if os.path.isfile(file1_path):
                os.remove(file1_path)
        
        
