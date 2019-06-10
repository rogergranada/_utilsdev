#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import cv2
import imutils
import numpy as np
from os.path import realpath, join, basename, splitext, dirname


def convert_raw_map(pgmfile, pathout, threshold=200):
    """ Convert and reduce the PGM file into a PNG file.
        The new size of the image is (2*threshold x 2*threshold)
    """
    pgmfile = realpath(pgmfile)
    image = cv2.imread(pgmfile, -1)
    x, y = image.shape
    center_x = x/2
    center_y = y/2
    left = center_x - threshold
    right = center_x + threshold
    up = center_y - threshold
    down = center_y + threshold 
    cropped = image[left:right,up:down]
    cv2.imwrite(pathout, cropped)


def main(imgfile):
    imgfile = realpath(imgfile)
    image = cv2.imread(imgfile)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 100, 200)
    #thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
 
    cnts = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        M = cv2.moments(c)
        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))

        print cX, cY
        cv2.circle(edges, (cX, cY), 5, (255,255,255), -1)
        c = c.astype("float")
        c = c.astype("int")
        #cv2.drawContours(image, [c], -1, (255, 0, 0), 2)
    
    cv2.imshow("image", edges)
    cv2.waitKey(0)
    cv2.destroyWindow('image')
    cv2.waitKey(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('image', metavar='imgfile', help='File containing the PGM image.')
    args = parser.parse_args()
    main(args.image)
