#!/usr/bin/python
#-*- coding: utf-8 -*-
 
import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments

import logging
logger = logging.getLogger('geo')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

# Set standard output encoding to UTF-8.
from codecs import getwriter
sys.stdout = getwriter('UTF-8')(sys.stdout)
import os
import time
import math
from os.path import join
from codecs import open
import re


def main(argv):
    t1 = time.time()
    home = '/home/roger/Desktop/tmp/'
    
    fout = open(join(home, 'out.txt'), 'w', 'utf-8')

    dic = {}
    with open(join(home, 'refer.txt'), 'r', 'utf-8') as fin:
        for line in fin:
            line = line.strip()
            bib, ref = line.strip().split('#')
            dic[bib] = ref

    with open(join(home, 'text.tex'), 'r', 'utf-8') as fin:
        for line in fin:
            for i in range(0,10):
                line = line.replace(str(i)+'}', str(i)+']')
            line = line.replace('\etc', 'etc.')
            line = line.replace('\emph{', '')
            line = line.replace('\idest', 'i.e.')
            line = line.replace('``', '"')
            line = line.replace("''", '"')
            line = line.replace('~', ' ')
            line = line.replace('\item', '*')
            line = line.replace('\cite{', '[')
            for el in dic:
                line = line.replace(el, dic[el])
            fout.write('%s\n' % line)

    fout.close()
    t2 = time.time()
    total_time = (t2 - t1) / 60
    logger.info('Processing time: %f minutes.' % total_time)    


if __name__ == "__main__":
    main(sys.argv)
