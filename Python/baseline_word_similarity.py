#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module implements the generation of a baseline to
cross-lingual distributional similarity model. The baseline
is composed by pairs of words (English - French) and a 
similarity score. This similarity score is based on the
distance in WordNet between the term in English and the 
most frequent translation to the French term. 

To run this script the user must have the NLTK and the 
WordNet in NLTK installed. To install WordNet in NLTK
type in python 
>>> nltk.download()
In the Corpora tab, select 'WordNet' and then 'Download'.

The input file is composed by the terms in English, French
and the translation of the French word as follows:

English_word [\t] French_word (Translation) [\t] Human_score

The output file contain the same input file but with three 
different WordNet similarity scores appended in each line. 
The similarity scores are:

- Path_similarity: Return a score denoting how similar 
two word senses are, based on the shortestpath that 
connects the senses in the is-a (hypernym/hypnoym) taxonomy.										
- Leacock-Chodorow Similarity: Return a score denoting how 
similar two word senses are, based onthe shortest path that 
connects the senses (as above) and the maximum depth of the 
taxonomy inwhich the senses occur. The relationship is given 
as -log(p/2d) where p is the shortest path lengthand d the 
taxonomy depth.										
- Wu-Palmer Similarity: Return a score denoting how similar 
two word senses are, based on the depthof the two senses in 
the taxonomy and that of their Least Common Subsumer (most 
specific ancestor node).											


Created on Aug 28, 2012

@author: granada
"""

import logging
import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.arguments

# Set standard output encoding to UTF-8.
from codecs import getwriter
sys.stdout = getwriter('UTF-8')(sys.stdout)
import os
import time
import re

import nltk
from nltk.corpus import wordnet

from utils.arguments import Arguments
from os.path import join
from codecs import open

logger = logging.getLogger('similarity.baseline')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

def main(argv):
    t1 = time.time()
    desc = "Takes a file containing pairs of words \
(English - OtherLanguage) and a second file containing \
the translation to the OtherLanguage words, and get three \
similarity scores based on WordNet to each pair."
    
    required = [desc, 'inputfile', 'outputfile']
    obj_args = Arguments(required)
    logger.info(obj_args)
    args = obj_args.getArgs()

    comments = """# This file is composed by the list of terms
# from the papers of Rubenstein and Goodenough (1965) and
# Joubarne and InkPen (2011). The pairs are composed as the
# first word of Goodenough and the second word of Joubarne pairs.
# The word in parentesis is the most frequent translation to the
# French word. The score is the average of the scores of both 
# pairs. For instance, the score to the pair "cord - sourire" 
# is the average between the scores of the pairs "cord - smile 
# = 0.02" (Rubenstein and Goodenough) and "corde - sourire = 0.00" 
# (Joubarne and InkPen). All pairs can be found on the page:
# http://www.site.uottawa.ca/~mjoub063/wordsims.htm\n#
# References:
# - Rubenstein, H. and J. B. Goodenough. “Contextual correlates of
# synonymy.”, Communications of the ACM 8(10), 1965, pp. 627–633.
# - Joubarne, C. and InkPen, D. "Comparison of Semantic Similarity
# for Different Languages Using the Google n-gram Corpus and Second-
# Order Co-occurrence Measures", Advances in Artificial Intelligence,
# v. 6657, 2011, pp. 216-221.\n#
# The pairs are organized as follows:
# English_word [\\t] French_word (English_translation) [\\t] Human_score [\\t]
# Path_similarity [\\t] Leacock-Chodorow_similarity[\\t] Wu-Palmer_similarity [\\n]\n#\n"""

    regex_tr = re.compile('\((\w+)\)')
    args.outputfile.write(comments)
    for line in args.inputfile:
        if not "#" in line: # Skip comments
            term_1, term_2, human_score = line.strip().split('\t')
            translation = regex_tr.search(term_2).group(1)
            synset_1 = wordnet.synset(term_1+'.n.01')
            synset_2 = wordnet.synset(translation+'.n.01')
            logger.info('calculating similarity to the pair: %s %s' % (term_1, term_2.decode('utf-8')))

            # Similarity measures
            path_sim = synset_1.path_similarity(synset_2)
            lch_sim = synset_1.lch_similarity(synset_2)
            wup_sim = synset_1.wup_similarity(synset_2)
            args.outputfile.write('%s\t%s\t%s\t%f\t%f\t%f\n' % (term_1, term_2, human_score, path_sim, lch_sim, wup_sim))

    t2 = time.time()
    total_time = (t2 - t1) / 60
    logger.info('processing time: %f minutes.' % total_time)   

if __name__ == "__main__":
	main(sys.argv[1:])

