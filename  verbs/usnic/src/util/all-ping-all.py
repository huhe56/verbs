'''
Created on Aug 19, 2013

@author: huhe
'''

import re

from main.define import Define
from lib.util import Util


def get_node_list():
    pattern1 = re.compile(r",")
    pattern2 = re.compile("\[(?P<range>[0-9\-]+)\]")
    pattern3 = re.compile(r"-")
    node_list = []
    config_file_path = Define.PATH_USNIC_CONFIG + "ping.cfg"
    line_list = Util.read_file(config_file_path)
    for line in line_list:
        line.strip()
        if pattern1.search(line):
            node_list_1 = pattern1.split(line)
            node_list = node_list + node_list_1
        elif pattern2.search(line):
            m = pattern2.search(line)
            rangex = m.group("range")
            hostname_prefix = line.replace("[" + rangex + "]", "")
            range_item_list = pattern3.split(rangex)
            for i in range(int(range_item_list[0]), int(range_item_list[1])):
                i_str = None
                if i < 10: i_str = "0" + str(i)
                else: i_str = str(i)
                hostname = hostname_prefix + i_str
                node_list.append(hostname)
        else:
            node_list.append(line)
    return sorted(node_list)

    
if __name__ == '__main__':
    node_list = get_node_list()
    print node_list
    
    
                