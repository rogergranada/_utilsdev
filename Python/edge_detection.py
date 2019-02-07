#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse
import numpy as np
import cv2

def main(imagefile):
    scale = 5
    delta = 5
    ddepth = cv2.CV_8U
    img = cv2.imread(imagefile, 0)
    sobelx = cv2.Sobel(img, ddepth,1,0,ksize = 3, scale = scale, delta = delta,borderType = cv2.BORDER_DEFAULT)
    #sobelx = cv2.Sobel(img, cv2.CV_8U,1,0,ksize=5)
    #sobely = cv2.Sobel(img, cv2.CV_8U,0,1,ksize=5)
    cv2.imshow('image',sobelx)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='file_input', help='the file received as input.')
    args = parser.parse_args()

    main(args.inputfile)
