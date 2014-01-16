'''
Created on Aug 8, 2013

@author: huhe
'''

import shutil, os

from utils.utils import Utils


if __name__ == '__main__':
    
    print Utils.get_current_time_string()
    
    dir1 = '/home/huhe/workspace/usnic/log/'
    dir2 = '/home/huhe/workspace/usnic/log/tmp'
    
    files = os.listdir(dir1)
    for file1 in files:
        print file1
        if os.path.isfile(dir1 + file1):
            shutil.move(dir1 + file1, dir2)