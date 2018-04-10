#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
from codecs import open
import pymongo
from pymongo import Connection

def main():
    #connection = Connection('localhost')
    #db = connection['dsm_corpora']
    #col = db['wikipt']
    with open('/media/Musics/WikiPT/documents.txt', 'r', 'utf-8') as fin:
        with open('/media/Musics/WikiPT/documents2.txt', 'w', 'utf-8') as fout:
            fin.next()
            for n, line in enumerate(fin):
                if n % 100000 == 0 and n != 0:
                    print 'processing file %d' % n
                arr = line.strip().split()
                id1 = arr[0]
                id2 = arr[1]
                title = ' '.join(arr[2:])
                #query = col.find({'_id':id2}, timeout=False)
                #if query.count() == 0:
                #    print 'ERROR: ID %s' % id2
                #else:
                #    fout.write(id1+' '+id2+' "'+query.next()['title']+'"\n')
                fout.write(id1+' '+id2+' "'+title+'"\n')

if __name__ == "__main__":
    main()
