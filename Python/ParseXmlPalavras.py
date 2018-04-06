#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import sys
import codecs

class ParseXml:

	def __init__(self, filename):
		self.dic_t = {}
		self.dic_nt = {}
		self.dic_nts = {}
		self.dic_nouns = {}
		self.dic_verbs = {}
		
		self.buidStructure = True
		self.buidNouns = True
		self.buidVerbs = True

		self.__buildDics__(filename)

	def __buildDics__(self, filename):
		try:
			xmlfile = codecs.open(filename, 'r', 'utf-8')
		except IOError:
			print 'ERROR: System cannot open the '+filename+' file'
			sys.exit()

		for line in xmlfile:
			if '<t ' in line:
				id_t = (line.split('id=\"')[1]).split('\"')[0]
				word = (line.split('word=\"')[1]).split('\"')[0].lower()
				lemma = ((line.split('lemma=\"')[1]).split('\"')[0]).lower()
				morph = (line.split('morph=\"')[1]).split('\"')[0]
				sem = (line.split('sem=\"')[1]).split('\"')[0]
				extra = (line.split('extra=\"')[1]).split('\"')[0]
				
				if re.search('%|&amp;', lemma):
					pos = '--' 
				else:
					pos = (line.split('pos=\"')[1]).split('\"')[0]

				self.dic_t[id_t] = {'word':word, 'lemma':lemma, 'pos':pos, 'morph':morph, 'sem':sem, 'extra':extra, 'headof':''}
				
			elif '<nt ' in line:
				id_nt = (line.split('id=\"')[1]).split('\"')[0]
				id_nt_number = id_nt.split('_')[1]
				cat = (line.split('cat=\"')[1]).split('\"')[0]
				array_edges = []
				self.dic_nt[id_nt] = {'cat':cat, 'edge':array_edges}
			
			elif '<edge ' in line:
				
				idref = (line.split('idref=\"')[1]).split('\"')[0]
				idref_number = idref.split('_')[1]
				label = (line.split('label=\"')[1]).split('\"')[0]
				if int(idref_number) < 500 or int(idref_number) > int(id_nt_number):
					array_edges.append([idref, label])
				
				if label == 'H':
					self.dic_t[idref]['headof'] = id_nt
					self.dic_nt[id_nt]['head'] = idref

			elif '</nt>' in line:
				self.dic_nt[id_nt]['edge'] = array_edges
		
		xmlfile.close()

	def __buildNonTerminalStructure__(self):
		for id_nt in self.dic_nt:
			list_np = []
			for idref in self.dic_nt[id_nt]['edge']:
				list_np.append(idref[0])
			
			inner_count = 0
			while inner_count < len(list_np):
				idref = list_np[inner_count]
				idref_number = int(list_np[inner_count].split('_')[1])
				
				if int(idref_number) > 500:
					list_np.pop(inner_count)
					temp_count = inner_count
					for idref_inner in self.dic_nt[idref]['edge']:
						list_np.insert(temp_count, idref_inner[0])
						temp_count = temp_count + 1					
					inner_count = inner_count - 1
				inner_count = inner_count + 1

			self.dic_nts[id_nt] = {'structure': list_np}

		for id_nts in self.dic_nts:
			phrase = ''
			for id_t in self.dic_nts[id_nts]['structure']:
				phrase += self.dic_t[id_t]['lemma']+' '
			self.dic_nts[id_nts]['phrase'] = phrase.rstrip()

		self.buidStructure = False

	def __buildDicNouns__(self):
		for id_t in self.dic_t:
			if re.match('^(n|prop)$', self.dic_t[id_t]['pos']):
				self.dic_nouns[id_t] = self.dic_t[id_t]['lemma']
		self.buidNouns = False
	
	def __buildDicVerbs__(self):
		for id_t in self.dic_t:
			if re.match('^v-', self.dic_t[id_t]['pos']):
				self.dic_verbs[id_t] = self.dic_t[id_t]['lemma']
		self.buidVerbs = False

	def getDicTerms(self):
		return self.dic_t

	def getTermsById(self, id_t):
		try:
			term = self.dic_t[id_t]
		except:
			print 'ERROR: Term with ID '+id_t+' was not found'
			sys.exit()
		return term

	def getDicNonTerminals(self):
		return self.dic_nt

	def getNonTerminalsById(self, id_nt):
		try:
			nonterminal = self.dic_nt[id_nt]
		except:
			print 'ERROR: Non terminal with ID '+id_nt+' was not found'
			sys.exit()
		return nonterminal

	def getDicNTStructure(self):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
		return self.dic_nts

	def getDicNTStructureToNP(self):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
		dic_nts_np = {}
		for id_nts in self.dic_nts:
			if self.dic_nt[id_nts]['cat'] == 'np':
				dic_nts_np[id_nts] = self.dic_nts[id_nts]
		return dic_nts_np

	def getNTStructureById(self, id_nts):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
		try:
			nts = self.dic_nts[id_nts]
		except:
			print 'ERROR: Non terminal structure with ID '+id_nts+' was not found'
			sys.exit()
		return nts

	def getNouns(self):
		if self.buidNouns:
			self.__buildDicNouns__()
		return self.dic_nouns

	def getListNouns(self):
		if self.buidNouns:
			self.__buildDicNouns__()
		list_nouns = {}
		for id_t in self.dic_nouns:
			list_nouns[self.dic_nouns[id_t]] = self.dic_nouns[id_t]
		return list_nouns

	def getVerbs(self):
		if self.buidVerbs:
			self.__buildDicVerbs__()
		return self.dic_verbs

	def getListVerbs(self):
		if self.buidVerbs:
			self.__buildDicVerbs__()
		list_verbs = {}
		for id_t in self.dic_verbs:
			list_verbs[self.dic_verbs[id_t]] = self.dic_verbs[id_t]
		return list_verbs
	
	def printDicTerms(self):
		for id_t in self.dic_t:
			print 'Key: '+id_t
			print self.dic_t[id_t]
			print '\n'

	def printTermsById(self, id_t):
		try:
			term = self.dic_t[id_t]
		except:
			print 'ERROR: Term with ID '+id_t+' was not found'
			sys.exit()
		print term

	def printDicNonTerminals(self):
		for id_nt in self.dic_nt:
			print 'Key: '+id_nt
			print self.dic_nt[id_nt]

	def printNonTerminalsById(self, id_nt):
		try:
			nonterminal = self.dic_nt[id_nt]
		except:
			print 'ERROR: Non terminal with ID '+id_nt+' was not found'
			sys.exit()
		print nonterminal

	def printDicNTStructure(self):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
		for id_nts in self.dic_nts:
			print 'Key: '+id_nts
			print self.dic_nts[id_nts]

	def printDicNTStructureToNP(self):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
		for id_nts in self.dic_nts:
			if self.dic_nt[id_nts]['cat'] == 'np':
				print self.dic_nts[id_nts]

	def printNTStructureById(self, id_nts):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
		try:
			nts = self.dic_nts[id_nts]
		except:
			print 'ERROR: Non terminal structure with ID '+id_nts+' was not found'
			sys.exit()
		print nts

	def printNouns(self):
		if self.buidNouns:
			self.__buildDicNouns__()
		for id_noun in self.dic_nouns:
			print 'Key: '+id_noun
			print self.dic_nouns[id_noun]

	def printVerbs(self):
		if self.buidVerbs:
			self.__buildDicVerbs__()
		for id_verb in self.dic_verbs:
			print 'Key: '+id_verb
			print self.dic_verbs[id_verb]

	def printListNouns(self):
		if self.buidNouns:
			self.__buildDicNouns__()
		list_nouns = {}
		for id_t in self.dic_nouns:
			list_nouns[self.dic_nouns[id_t]] = self.dic_nouns[id_t]
		for noun in list_nouns:
			print noun+', ',

	def printListVerbs(self):
		if self.buidVerbs:
			self.__buildDicVerbs__()
		list_verbs = {}
		for id_t in self.dic_verbs:
			list_verbs[self.dic_verbs[id_t]] = self.dic_verbs[id_t]
		for verb in list_verbs:
			print verb+', ',
