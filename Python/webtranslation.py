#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
Translate components
""" 
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import argparse
from googletrans import Translator
from os.path import dirname, splitext, basename, join
import codecs

import progressbar

def count_lines(inputfile):
    #count lines
    lines = 0
    with open(inputfile) as fin:
        for _ in fin:
            lines += 1
    return lines


def list_of_words(inputfile):
    lines = count_lines(inputfile)
    
    dic = {}
    pb = progressbar.ProgressBar(lines)
    with open(inputfile) as fin:
        for line in fin:
            w1, type, rel, w2 = line.strip().split('\t')
            if not dic.has_key(w1):
                dic[w1] = ''
            if not dic.has_key(type):
                dic[type] = ''
            if not dic.has_key(rel):
                dic[rel] = ''
            if not dic.has_key(w2):
                dic[w2] = ''
    return dic.keys()
            

def main(inputfile):
    """
    pistol-n \t weapon \t random-v \t start-v
    """
    dirin = dirname(inputfile)
    fname, ext = splitext(basename(inputfile))

    # create a list of words
    words = list_of_words(inputfile)
    
    fout = codecs.open(join(dirin, fname+'_dic.txt'), 'w', 'utf-8')
    translator = Translator()
    for word in words:
        word_pt = translator.translate(word, dest='pt')
        fout.write('%s %s\n' % (word, word_pt))
    
    """
    lines = count_lines(inputfile)

    pb = progressbar.ProgressBar(lines)
    lastw = ''
    with open(inputfile) as fin:
        for line in fin:
            w1, type, rel, w2 = line.strip().split('\t')
            #print w1, rel, w2, '->', type
            if w1 != lastw:
                translator = Translator()
                lastw = w1
            
            w1_pt = translator.translate(w1, dest='pt')
            w2_pt = translator.translate(w2, dest='pt')
            type_pt = translator.translate(type, dest='pt')
            rel_pt = translator.translate(rel, dest='pt')

            fout.write('%s %s %s %s\n' % (w1_pt.text, type_pt.text, rel_pt.text, w2_pt.text))
            pb.update()
    """
    fout.close()

# End of Translation class

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='file_input', help='file containing text to translate.')
    args = parser.parse_args()

    main(args.inputfile)
