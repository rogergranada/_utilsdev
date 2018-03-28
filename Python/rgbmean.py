#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse
import cv2

def getRGBMeans(filein):
    """
    Extract the mean of RGB channels from image files.

    Parameters:
    -----------
    filein : string
        Input file containing the path to all images
    """
    mean_B = 0.0
    mean_G = 0.0
    mean_R = 0.0
    with open(filein) as fin:
        for n, line in enumerate(fin):
            path, label = line.strip().split()
            
            bgr_img = cv2.imread(path)
            b,g,r = cv2.split(bgr_img)
            mean_B += b.mean()
            mean_G += g.mean()
            mean_R += r.mean()
            
    n += 1
    print 'Mean B:', mean_B/n
    print 'Mean G:', mean_G/n
    print 'Mean R:', mean_R/n


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='file_input', help='the file received as input.')
    args = parser.parse_args()

    getRGBMeans(args.inputfile)
