#!/opt/local/anaconda2/bin/python
import os,time,datetime
import re
from collections import defaultdict

pydir =  os.path.dirname(os.path.abspath(__file__))

file = os.path.join(pydir,"nsc_oscaps.list")

def getFileAsList(file):
    #return [tuple(line.rstrip('\n').split()) for line in open(file) if not line.startswith('#')]
    if os.path.exists(file):
        in_list = [line.rstrip('\n').split() for line in open(file) if not (line.startswith('#') or line.rstrip('\n').split() == []) ]
        if len(in_list) < 0:
            print "WARNING: %s is empty or has no valid lines !!" % file
        return in_list
    else:
        print "WARNING: %s doesn't existt !!" % file
        return []


def getFileAsDictOfLists(file):
    '''return dict from file with line format "index item1,item2, ..." '''
    in_list = getFileAsList(file)
    in_dict = defaultdict(list)
    if len(in_list) < 0:
        return None
    else:
        for index, value in in_list:
            in_dict[index] = value.split(',')
        return in_dict

dict = getFileAsDictOfLists(file)

print dict