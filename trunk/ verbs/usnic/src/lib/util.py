'''
Created on Aug 8, 2013

@author: huhe
'''

import logging
import os
import re


class Util(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    @staticmethod
    def getLogger(filename):
        logger = logging.getLogger(os.path.basename(filename));
        logger.propagate = False
        if (len(logger.handlers) == 0):
            # formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
            '''
            mkdir(Define._PathLog)
            loggerHandler2 = logging.FileHandler(Define._PathLogFile)
            loggerHandler2.setFormatter(formatter)
            logger.addHandler(loggerHandler2)
            '''
            
            loggerHandler = logging.StreamHandler()
            loggerHandler.setFormatter(formatter)
            logger.addHandler(loggerHandler)
            
            logger.setLevel(logging.DEBUG)
            
        return logger


    @staticmethod
    def find_pattern_list(pattern, string):
        print pattern
        m = re.findall(pattern, string)
        print "---------" 
        print m
        
        