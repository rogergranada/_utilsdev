#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import codecs
from numpy import *
from numpy.linalg import svd
from Parameters import Parameters

class SVD(object):

	def __init__(self, file_A):
		parameters = Parameters()
		svd_threshold = parameters.getSVDThreshold()
		
		try:
			file_matrix_A = codecs.open(file_A, 'r', 'utf-8')
		except IOError:
			print('ERROR: System cannot open the %s file' % file_A)
			sys.exit()

		loaded_A = file_matrix_A.read()
		A = array(loaded_A) # A is a (2x3) matrix ([[1., 3., 5.],[2., 4., 6.]])
		U, sigma, V = svd(A)
		sigma_reduced = zeros_like(A) # constructing Sigma from sigma
		sigma_reduced[:svd_threshold, :svd_threshold] = diag(sigma)
		print dot(U,dot(sigma_reduced,V)) # A = U * Sigma * V

