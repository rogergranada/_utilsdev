#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This class connects with Microsof Translation API and generates translations
for phrases passed as parameters in 'getTranslation() function.

Created on Feb 24, 2013
@author: granada
""" 

import sys
sys.path.insert(0, '..') # This line is inserted to find the package utils.msmt

# Set standard output encoding to UTF-8.
from codecs import getwriter, open
sys.stdout = getwriter('UTF-8')(sys.stdout)
import time

import logging
logger = logging.getLogger('interlinks')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from utils import Arguments, msmt
from utils.ontology import OWL

USER = 'roger'
TOKEN = ''

class Translation():
    def __init__(self):
        self.token = msmt.get_access_token(USER, TOKEN)

    def getTranslation(self, phrase, source_lang, target_lang):
        response = msmt.translate(self.token, phrase, target_lang, source_lang)
        if response:
            concept = response.split('>')[1].split('<')[0]
            if '\'' in concept:
                concept = concept.replace('\'', '&#39;')
            return concept
        else:
            return None

# End of Translation class

def main(args):
    t1 = time.time()
    desc = "Get ids of Wikipedia articles and store in the database. \
The database is composed by ID and TITLE of each article. The current \
implementation works only with the MongoDB database."

    required = [desc, 'inputfile', 'outputfile', 'language']
    obj_args = Arguments(required)
    logger.info(obj_args)
    args = obj_args.getArgs()

    handler = OWL(args.inputfile, args.outputfile)
    webapi = Translation()

    for source_language, label in handler:
        #print source_language, label
        translated = webapi.getTranslation(label.lower(), source_language, args.language)
        if translated != None:
            logger.info('Inserting concept [%s]: %s' % (label, translated))
            handler.insert(translated.lower(), args.language)
        else:
            handler.insert('NULL', args.language)
            logger.info('Concept not found: %s' % label.title())        

if __name__ == "__main__":
    main(sys.argv)
