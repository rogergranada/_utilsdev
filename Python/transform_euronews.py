#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
@author: granada
""" 

import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments

# Set standard output encoding to UTF-8.
from codecs import getwriter, open
sys.stdout = getwriter('UTF-8')(sys.stdout)
from os.path import join
import time
from xml.sax import make_parser
from parsexml import ParseSax
import shelve

import logging
logger = logging.getLogger('indexing.indexparallel')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def transform2gensim(dirin):
    """
    Add to mm file +1 in each document and each term.
    """
    fout = open(join(dirin, 'corpus_n.mm'), 'w', 'utf-8')
    with open(join(dirin, 'corpus.mm'), 'r', 'utf-8') as fin:
        for n, line in enumerate(fin):
            if n != 0 and n % 10000 == 0:
                logger.info('processing line: %d' % n)
            if line.startswith('%'):
                fout.write(line)
            else:
                iddoc, idt, f = map(int, line.strip().split())
                iddoc += 1
                idt += 1
                fout.write('%d %d %d\n' % (iddoc, idt, f))
    fout.close()

    fout = open(join(dirin, 'dictionary.txt'), 'w', 'utf-8')
    with open(join(dirin, 'corpus.dct'), 'r', 'utf-8') as fin:
        fin.next()
        for n, line in enumerate(fin):
            if n != 0 and n % 10000 == 0:
                logger.info('processing line: %d' % n)
            if line.startswith('%'):
                break
            else:
                id, t, f = line.strip().split()
                fout.write('%s\t%s\t%s\n' % (id, t, f))
    fout.close()

def build_db(dirin):
    t1 = time.time()
    # Parse the XML files using SAX
    parser = make_parser()   
    handler = ParseSax()
    parser.setContentHandler(handler)
    filein = join(dirin, 'ted_pt-br.xml')
    #db = shelve.open(join(dirin, 'ted.db'), 'n', writeback=True)

    logger.info('loading file: ted_pt-br.xml')
    with open(filein, 'r', 'utf-8') as fin:
        for n, line in enumerate(fin):
            if n != 0 and n % 10000 == 0:
                logger.info('processing line: %d' % n)
            parser.feed(line.strip().encode('utf-8'))
            if '</file>' in line:
                id, title, content = handler.getContent()
                with open(join(dirin, 'files', str(id)+'.txt'), 'w', 'utf-8') as fout:
                    fout.write(content)
                #db[str(id)] = content
    t2 = time.time()
    total_time = (t2 - t1) / 60
    logger.info('Processing time: %f minutes.' % total_time)

if __name__ == "__main__":
    build_db('/media/Diversos/PhD/PT/TED/')
