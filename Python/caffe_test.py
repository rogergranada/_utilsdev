#!/usr/bin/python
#-*- coding: utf-8 -*-

import subprocess
import sys
import os
import re
import time
from progressBar import ProgressBar

def update_progress(progress, total):
    #print progress, total
    print '\r[{0}] {1}%'.format('#'* ( int((float(progress)/total)*10)), progress) + ' / 100%'


if len(sys.argv) < 6:
	print "USAGE: [MODEL] [WEIGHTS_PATH] [GPU] [ITERATIONS] [OUTPUT_FILE]"
	sys.exit(0)

caffe_command    = "caffe test "
caffe_model      = "-model " + sys.argv[1] + " "
weights_path     = sys.argv[2]
caffe_weights    = "-weights " + weights_path
caffe_gpu        = "-gpu " + sys.argv[3] + " "
caffe_iterations = "-iterations " + sys.argv[4]
output_file_path = sys.argv[5]

while True:
	output_file = open(output_file_path, "r", 0)
	tested_models = []
	for line in output_file.readlines():
		line = line.strip()
		if ".caffemodel" not in line:
			continue
		tested_models += [re.findall("\d+", line)[-1]]
	output_file.close()

	output_file = open(output_file_path, "a", 0)
    
	qt = os.listdir(weights_path)
	pb = ProgressBar(len(qt)/2)
	for k, weight_file in enumerate(sorted(qt)):

		if "caffemodel" not in weight_file:
			continue
		
		iteration = re.findall("\d+", weight_file)[-1]
		
		if iteration in tested_models:
	#		print iteration, "model already tested. Skip this model!"
			continue		

#		print "-----> Processing model", iteration, "<-----"
		#update_progress((k+1)/2,len(qt)/2)
		pb.update()
		caffe_weights = "-weights " + os.path.join(weights_path, weight_file) + " "
		command       = caffe_command + caffe_model + caffe_weights + caffe_gpu + caffe_iterations
		output_file.write("Testing model " + weight_file + "\n")
		p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		loss = []
		accuracy = []
		while True:
			line = p.stdout.readline()
			if not line:
				break
			line = line.strip()
#			print "->", line		
			if len(loss) == 0:
				loss = re.findall("Loss: \d+[\.]?\d*", line)
			if len(accuracy) == 0:
#				print "-->" + line
				accuracy = re.findall("292] accuracy = \d+[\.]?\d*", line)
#				accuracy = re.findall("] loss3/top-1 = \d+[\.]?\d*", line)	
#		print "Model:", weight_file
		output_file.write("Model: " + weight_file + "\n")
#		print loss[-1]
		output_file.write(loss[-1] + "\n")
		#print accuracy [-1][2:]
		output_file.write(accuracy[-1][5:] + "\n")
#		print "-"*len("Model: " + weight_file)
		output_file.write("-"*len("Model: " + weight_file) + "\n")
		p.wait()
	output_file.close()

#	print "-----> Waitting 5 minutes for new models! <-----"
	time.sleep(300)
