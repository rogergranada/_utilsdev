#!/usr/bin/python

import math
import codecs
import sys

from collections import defaultdict
from operator import itemgetter

class Measures:
	def __init__(self, seed_rel_file, ctx_freq_file):
		self.dic_baseline = defaultdict(dict)
		self.dic_diceBin = defaultdict(dict)
		self.dic_diceMin = defaultdict(dict)
		self.dic_jaccard = defaultdict(dict)
		self.dic_cosineBin = defaultdict(dict)
		self.dic_cosine = defaultdict(dict)
		self.dic_city = defaultdict(dict)
		self.dic_euclidean = defaultdict(dict)
		self.dic_js = defaultdict(dict)
		self.dic_lin = defaultdict(dict)
		self.dic_jaccardMax = defaultdict(dict)
		self.dic_ctx = defaultdict(dict)
		self.dic_sum_freq_noun = {}
		self.dic_qty_noun = {}
		self.__buildHashs__(seed_rel_file, ctx_freq_file)
		

	def __buildHashs__(self, seed_rel_file, ctx_freq_file):
		try:
			seedfile = codecs.open(seed_rel_file, 'r', 'utf-8')
		except IOError:
			print 'ERROR: System cannot open the '+seed_rel_file+' file'
			sys.exit()
		try:
			ctxfreqfile = codecs.open(ctx_freq_file, 'r', 'utf-8')
		except IOError:
			print 'ERROR: System cannot open the '+ctx_freq_file+' file'
			sys.exit()
		
		for line in ctxfreqfile:
			modifier, noun, freq = line.split('#')
			freq = freq.replace('\n', '')
			self.dic_ctx[noun][modifier] = int(freq)
			if self.dic_sum_freq_noun.has_key(noun):
				self.dic_sum_freq_noun[noun] += int(freq)
			else:
				self.dic_sum_freq_noun[noun] = int(freq)
			if self.dic_qty_noun.has_key(noun):
				self.dic_qty_noun[noun] += 1
			else:
				self.dic_qty_noun[noun] = 1

		for line in seedfile:
			seed, related = line.split('#')
			related = related.replace('\n', '')
			baseline = 0
			diceBin = 0
			diceMin = 0
			jaccard = 0
			cosineBin = 0
			cosine = 0
			city = 0
			euclidean = 0
			js = 0
			lin = 0
			jaccardMax = 0

			sun_min = 0
			sun_max = 0
			sum_intersection = 0
			intersection = 0
			square_freq_seed = 0
			square_freq_related = 0
			d_seed = 0
			d_related = 0

			for modifier in self.dic_ctx[seed]:
				freq_seed_modifier = 0
				freq_related_modifier = 0
				if self.dic_ctx[related].has_key(modifier):
					baseline += 1
					freq_seed_modifier = self.dic_ctx[seed][modifier]
					freq_related_modifier = self.dic_ctx[related][modifier]
					sun_min += min(freq_seed_modifier, freq_related_modifier)
					sun_max += max(freq_seed_modifier, freq_related_modifier)
					city += abs(freq_seed_modifier - freq_related_modifier)
					euclidean += (freq_seed_modifier - freq_related_modifier)**2

					relative_freq_seed = float(freq_seed_modifier) / self.dic_sum_freq_noun[seed]
					if self.dic_sum_freq_noun[related] == 0:
						print 'ERROR: Frequency of '+related+' is zero.'
					else:
						relative_freq_related = float(freq_related_modifier) / self.dic_sum_freq_noun[related]
						relative_freq_seed_related = float(relative_freq_seed + relative_freq_related) / 2

					if relative_freq_seed > 0.0 and relative_freq_seed_related > 0.0:
						d_seed += relative_freq_seed * math.log(float(relative_freq_seed / relative_freq_seed_related))
					if relative_freq_related > 0.0 and relative_freq_seed_related > 0.0:
						d_related += relative_freq_related * math.log(float(relative_freq_related / relative_freq_seed_related))
					intersection += freq_seed_modifier * freq_related_modifier
					sum_intersection += freq_seed_modifier + freq_related_modifier
					square_freq_seed += freq_seed_modifier**2
					square_freq_related += freq_related_modifier**2
				
				elif self.dic_ctx[seed].has_key(modifier):
					freq_seed_modifier = self.dic_ctx[seed][modifier]
					sun_max += freq_seed_modifier
					city += freq_seed_modifier
					euclidean += freq_seed_modifier**2
					square_freq_seed += freq_seed_modifier**2
				
			for modifier in self.dic_ctx[related]:
				if not self.dic_ctx[seed].has_key(modifier):
					freq_related_modifier = self.dic_ctx[related][modifier]
					sun_max += freq_related_modifier
					city += freq_related_modifier
					euclidean += freq_related_modifier**2
					square_freq_related +=  freq_related_modifier**2

			if sun_max > 0:
				jaccardMax = float(sun_min) / sun_max

			if self.dic_qty_noun.has_key(seed) and self.dic_qty_noun.has_key(related):
				diceBin = float(2*baseline) / (self.dic_qty_noun[seed] + self.dic_qty_noun[related])
				cosineBin = baseline / math.sqrt(float(self.dic_qty_noun[seed] * self.dic_qty_noun[related]))
				jaccard = float(baseline) / (self.dic_qty_noun[seed] + self.dic_qty_noun[related] - baseline)
			
			if self.dic_sum_freq_noun.has_key(seed) and self.dic_sum_freq_noun.has_key(related):
				diceMin = float((2*sun_min)) / (self.dic_sum_freq_noun[seed] + self.dic_sum_freq_noun[related])
				lin = float(sum_intersection) / (self.dic_sum_freq_noun[seed] + self.dic_sum_freq_noun[related])

			if square_freq_seed > 0 and square_freq_related > 0:
				cosine = intersection / (math.sqrt(float(square_freq_seed * square_freq_related)))
			euclidean = math.sqrt(float(euclidean))
			js = float(d_seed + d_related) / 2

			if  baseline >= 1:
				self.dic_baseline[seed][related] = baseline
				self.dic_diceBin[seed][related] = diceBin
				self.dic_diceMin[seed][related] = diceMin
				self.dic_jaccard[seed][related] = jaccard
				self.dic_cosineBin[seed][related] = cosineBin
				self.dic_cosine[seed][related] = cosine
				self.dic_city[seed][related] = city
				self.dic_euclidean[seed][related] = euclidean
				self.dic_js[seed][related] = js
				self.dic_lin[seed][related] = lin
				self.dic_jaccardMax[seed][related] = jaccardMax

	""" Methods to get the entire dictionaries """
	def getDicBaseline(self):
		return self.dic_baseline

	def getDicDiceBin(self):
		return self.dic_diceBin

	def getDicDiceMin(self):
		return self.dic_diceMin

	def getDicJaccard(self):
		return self.dic_jaccard

	def getDicCosineBin(self):
		return self.dic_cosineBin

	def getDicCosine(self):
		return self.dic_cosine

	def getDicCity(self):
		return self.dic_city

	def getDicEuclidean(self):
		return self.dic_euclidean

	def getDicJs(self):
		return self.dic_js

	def getDicLin(self):
		return self.dic_lin

	def getDicJaccardMax(self):
		return self.dic_jaccardMax

	""" Methods to get the dictionaries to a specific seed """
	def getDicBaselineToSeed(self, seed):
		return self.__existKeyInDic__(seed, self.dic_baseline)

	def getDicDiceBinToSeed(self, seed):
		return self.__existKeyInDic__(seed, self.dic_diceBin)

	def getDicDiceMinToSeed(self, seed):
		return self.__existKeyInDic__(seed, self.dic_diceMin)

	def getDicJaccardToSeed(self, seed):
		return self.__existKeyInDic__(seed, self.dic_jaccard)

	def getDicCosineBinToSeed(self, seed):
		return self.__existKeyInDic__(seed, self.dic_cosineBin)

	def getDicCosineToSeed(self, seed):
		return self.__existKeyInDic__(seed, self.dic_cosine)

	def getDicCityToSeed(self, seed):
		return self.__existKeyInDic__(seed, self.dic_city)

	def getDicEuclideanToSeed(self, seed):
		return self.__existKeyInDic__(seed, self.dic_euclidean)

	def getDicJsToSeed(self, seed):
		return self.__existKeyInDic__(seed, self.dic_js)

	def getDicLinToSeed(self, seed):
		return self.__existKeyInDic__(seed, self.dic_lin)

	def getDicJaccardMaxToSeed(self, seed):
		return self.__existKeyInDic__(seed, self.dic_jaccardMax)

	""" Methods to get the TOP N to a specific seed """
	def getTopNBaselineToSeed(self, seed, n):
		return self.__sortTopNFromDic__(self.dic_baseline, seed, n)

	def getTopNDiceBinToSeed(self, seed, n):
		return self.__sortTopNFromDic__(self.dic_diceBin, seed, n)

	def getTopNJaccardToSeed(self, seed, n):
		return self.__sortTopNFromDic__(self.dic_jaccard, seed, n)

	def getTopNCosineBinToSeed(self, seed, n):
		return self.__sortTopNFromDic__(self.dic_cosineBin, seed, n)

	def getTopNCosineToSeed(self, seed, n):
		return self.__sortTopNFromDic__(self.dic_cosine, seed, n)

	def getTopNCityToSeed(self, seed, n):
		return self.__sortTopNFromDic__(self.dic_city, seed, n)
	
	def getTopNEuclideanToSeed(self, seed, n):
		return self.__sortTopNFromDic__(self.dic_euclidean, seed, n)

	def getTopNJsToSeed(self, seed, n):
		return self.__sortTopNFromDic__(self.dic_js, seed, n)

	def getTopNLinToSeed(self, seed, n):
		return self.__sortTopNFromDic__(self.dic_lin, seed, n)

	def getTopNJaccardMaxToSeed(self, seed, n):
		return self.__sortTopNFromDic__(self.dic_jaccardMax, seed, n)


	""" Internal methods """
	def __sortTopNFromDic__(self, dic, seed, n):
		dic_terms = {}
		if self.__existKeyInDic__(seed, dic):
			for related_term in dic[seed]:
				dic_terms[related_term] = dic[seed][related_term]
			return sorted(dic_terms.items(), key=itemgetter(1), reverse=True)[0:n]

	def __existKeyInDic__(self, key, dic):
		if dic.has_key(key):
			return dic
		else:
			print 'ERROR: System cannot found the term "'+key+'" in dictionary'
			return False

if __name__ == '__main__':
	term = Measures('/home/roger/Programs/Portuguese-ATC/Temp/seedsToRelated.txt', '/home/roger/Programs/Portuguese-ATC/Temp/tempMergedFile.txt')
	print term.getTopNDiceBinToSeed('evento', 5)
