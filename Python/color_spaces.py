#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
HSV values in Gimp vary from 0-360 while in OpenCV these values vary from 0-180.
Thus, when adding values to the mask, get the half of Gimp values.

"""
import argparse
import numpy as np
import cv2

def standard_colors(color):
    if color == 'red':
        lower = np.array([169, 100, 100])
        upper = np.array([189, 255, 255])
    elif color == 'blue':
        lower = np.array([110, 50, 50])
        upper = np.array([130, 255, 255])
    elif color == 'green':
        lower = np.array([60,50,50])
        upper = np.array([80,255,255])
    elif color == 'orange':
        lower = np.array([5,50,50])
        upper = np.array([15,255,255])
    elif color == 'purple':
        lower = np.array([140,50,50])
        upper = np.array([160,255,255])
    elif color == 'yellow':
        lower = np.array([20,50,50])
        upper = np.array([40,255,255])
    else:
        lower = None
        upper = None
    return lower, upper


def color_spaces(img, space):
    if space == 'hsv':
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    elif space == 'lab':
        return cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    elif space == 'hls':
        return cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    elif space == 'luv':
        return cv2.cvtColor(img, cv2.COLOR_BGR2LUV)
    elif space == 'xyz':
        return cv2.cvtColor(img, cv2.COLOR_BGR2XYZ)
    elif space == 'ycrcb':
        return cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    elif space == 'yuv':
        return cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    else:
        return img


def hsv_from_rbg(r, g, b):
    """ red, green, blue """
    rgb = np.uint8([[[r, g, b]]])
    hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
    return hsv[0][0]


def cspaces(input):
    img = cv2.imread(input)
    cspace = color_spaces(img, 'hsv')
    lower, upper = standard_colors('yellow')
    mask = cv2.inRange(cspace, lower, upper)
    masked = cv2.bitwise_and(img, img, mask=mask)

    #cv2.imshow('image', img)
    cv2.imshow('masked', masked)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='file_input', help='the file received as input.')
    args = parser.parse_args()

    cspaces(args.inputfile)
