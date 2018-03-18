#!/usr/bin/python
#-*- coding: utf-8 -*-

import re

from pyPdf import PdfFileWriter, PdfFileReader

class Main:
	def __init__(self):
		input1 = PdfFileReader(file("/home/roger/Desktop/arquivo.pdf", "rb"))

		# print the title of document1.pdf
		print "title = %s" % (input1.getDocumentInfo().title)

		if not input1.isEncrypted:
			page4 = input1.getPage(5).extractText()
			page4 = " ".join(page4.replace(u"\xa0", " ").strip().split())
			page4 = page4.split('REFERENCES ')[1]
			print page4


		# print how many pages input1 has:
		print "document1.pdf has %s pages." % input1.getNumPages()

	def getPDFContent(path):
		content = ""
		num_pages = 5
		p = file(path, "rb")
		pdf = pyPdf.PdfFileReader(p)
		for i in range(0, num_pages):
			content += pdf.getPage(i).extractText() + "\n"
		content = " ".join(content.replace(u"\xa0", " ").strip().split())
		return content

if __name__ == '__main__':
	main = Main()
	
