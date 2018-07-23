#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import argparse
from os.path import realpath, dirname, join, isfile, isdir

def main():
    HOME='/home/roger/Desktop/Results.txt'

    with open(HOME) as fin:
        content = ''
        for line in fin:
            line = line.strip()
            if line:
                arr = line.split()
                content += arr[0]+'<br>'
            else:
                print content[:-4]
                content = ''

            


if __name__ == '__main__':
    main()
