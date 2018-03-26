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

# THRESHOLD to Cosine similarity
THRESHOLD = 0.1

def load_dicts(dicfile):
    dic = {}
    idic = {}
    with open(dicfile, 'r', 'utf-8') as fdic:
        for line in fdic:
            if not line.startswith('%%'):
                id, word, freq = line.strip().split()
                id = int(id)
                dic[id] = word
                idic[word] = id
    return dic, idic


class MmCorpus():
    def __init__(self, fname):
        self.fin = open(fname, 'r', 'utf-8')

    def __iter__(self):
        self.skip_headers()
        previd = -1
        for line in self.fin:
            idw, idf, freq = line.strip().split()
            idw, idf, freq = int(idw), int(idf), int(freq)
            if idw != previd:
                # change of document: return the document read so far (its id is prevId)
                if previd >= 0:
                    yield previd, word

                # from now on start adding fields to a new document, with a new id
                previd = idw
                word = []
            word.append((idf, freq))

        if previd >= 0:
            yield previd, word

    def skip_headers(self):
        self.fin.seek(0)
        self.fin.next()
        self.nw, self.nf, self.nnz = self.fin.next().split()

    def get_vecbyid(self, idq):
        self.skip_headers()
        word = []
        for line in self.fin:
            idw, idf, freq = line.strip().split()
            idw, idf, freq = int(idw), int(idf), int(freq)
            if idw == idq:
                word.append((idf, freq))
            elif idw > idq:
                break
        return word


def cossim(vec1, vec2):
    vec1, vec2 = dict(vec1), dict(vec2)
    if not vec1 or not vec2:
        return 0.0
    vec1len = 1.0 * math.sqrt(sum(val * val for val in vec1.itervalues()))
    vec2len = 1.0 * math.sqrt(sum(val * val for val in vec2.itervalues()))
    assert vec1len > 0.0 and vec2len > 0.0, "sparse documents must not contain any explicit zero entries"
    if len(vec2) < len(vec1):
        vec1, vec2 = vec2, vec1 # swap references so that we iterate over the shorter vector
    result = sum(value * vec2.get(index, 0.0) for index, value in vec1.iteritems())
    result /= vec1len * vec2len # rescale by vector lengths
    return result


def issubsumed(v1, v2):
    dic1 = dict(v1)
    dic2 = dict(v2)
    paeb = len(set(dic1.keys()) & set(dic2.keys()))
    pa = len(dic1)
    pb = len(dic2)
    pab = float(paeb) / pb
    pba = float(paeb) / pa
    if pab >= 0.4 and pba < 1:
        return 1
    elif pba >= 0.4 and pab < 1:
        return -1
    return 0

def main(argv):
    t1 = time.time()
    inputfolder = '/usr/local/EQ-MELODI/granada/geo/'
    #inputfolder = '/home/roger/Desktop/test/'
    dic, idic = load_dicts(join(inputfolder, 'dictionary.txt'))
    corpus = MmCorpus(join(inputfolder, 'cooccur.mm'))
    
    """
    # This part get the most similar terms to each seed
    fout = open(join(inputfolder, 'cosine.txt'), 'w', 'utf-8')
    with open(join(inputfolder, 'seeds.txt'), 'r', 'utf-8') as fseeds:
        for seed in fseeds:
            cosine = []
            seed = seed.strip()
            if idic.has_key(seed):
                vseed = corpus.get_vecbyid(idic[seed])
                for idw, vrel in corpus:
                    if idw != idic[seed]:
                        cosine.append((idw, cossim(vseed, vrel)))
            for idr, valcos in sorted(cosine, key=lambda cos: cos[1], reverse=True):
                if valcos > THRESHOLD:
                    fout.write('%s %s %f\n' % (seed, dic[idr], valcos))
    fout.close()
    """
    #After selecting some related terms to each seed
    #using the threshold 1.5, we verify if the term is
    #subsumed by the other
 
    dseed = {}
    with open(join(inputfolder, 'cosine.txt'), 'r', 'utf-8') as fin:
        for line in fin:
            seed, related, sim = line.strip().split()
            if dseed.has_key(seed):
                dseed[seed].append(related)
            else:
                dseed[seed] = [seed, related]

        for seed in dseed:
            fout = open(join(inputfolder, 'sbs_'+seed+'.txt'), 'w', 'utf-8')
            elem = dseed[seed]
            for i in range(len(elem)):
                for j in range(i+1,len(elem)):
                    e1 = elem[i]
                    e2 = elem[j]
                    vi = corpus.get_vecbyid(idic[e1])
                    vj = corpus.get_vecbyid(idic[e2])
                    #print 'verifying subsumed to pair [%s %s]' % (dic[i], dic[j])
                    subsumed = issubsumed(vi, vj)
                    if subsumed == 1:
                        fout.write('%s %s\n' % (e1, e2))
                    elif subsumed == -1:
                        fout.write('%s %s\n' % (e2, e1))
                    print 'verifying subsumed to pair [%s %s] %d' % (e1, e2, subsumed)
            fout.close()

    """ for unique seeds
    dseed = {}
    fout = open(join(inputfolder, 'subs_arenito.txt'), 'w', 'utf-8')
    with open(join(inputfolder, 'cos_arenito.txt'), 'r', 'utf-8') as fin:
        for line in fin:
            seed, related, sim = line.strip().split()
            if dseed.has_key(seed):
                dseed[seed].append(related)
            else:
                dseed[seed] = [seed, related]

        for seed in dseed:
            elem = dseed[seed]
            for i in range(len(elem)):
                for j in range(i+1,len(elem)):
                    e1 = elem[i]
                    e2 = elem[j]
                    vi = corpus.get_vecbyid(idic[e1])
                    vj = corpus.get_vecbyid(idic[e2])
                    #print 'verifying subsumed to pair [%s %s]' % (dic[i], dic[j])
                    subsumed = issubsumed(vi, vj)
                    if subsumed == 1:
                        fout.write('%s %s\n' % (e1, e2))
                    elif subsumed == -1:
                        fout.write('%s %s\n' % (e2, e1))
                    print 'verifying subsumed to pair [%s %s] %d' % (e1, e2, subsumed)
    fout.close()
    """
    # From the file hsubsumption, build a dictionary containing only
    # unique pairs of words. Then, test for each seed the relations and
    # record it in a separated file.
    """
    d_pairs = {}
    with open(join(inputfolder, 'hsubsumption.txt'), 'r', 'utf-8') as fin:
        for line in fin:
            line = line.strip()
            if not d_pairs.has_key(line):
                d_pairs[line] = line.replace('+', '_')
    #print d_pairs

    with open(join(inputfolder, 'cosarenito.txt'), 'r', 'utf-8') as fin:
        last = ''
        fout = None
        for line in fin:
            seed, related, sim = line.strip().split()
            if seed != last:
                if fout != None:
                    fout.close()
                print 'Creating file to seed %s: %s' % (seed, join(inputfolder, seed+'.txt'))
                fout = open(join(inputfolder, seed+'.txt'), 'w', 'utf-8')
                last = seed
            if d_pairs.has_key(seed+' '+related):
                print "YES"
                fout.write('%s\n' % (d_pairs[seed+' '+related]))
            #else:
                print seed+' '+related
    """
    t2 = time.time()
    total_time = (t2 - t1) / 60
    logger.info('Processing time: %f minutes.' % total_time)    


if __name__ == "__main__":
    main(sys.argv)
