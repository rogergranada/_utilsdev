#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This script computes the mean of a set of images for Caffe framework.
"""
import argparse
import numpy as np
import os

from caffe.io import array_to_blobproto
from skimage import io


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', type=str, help="Path to a text file containing the set of images.")
    parser.add_argument('outputfile', type=str, help="Name of the file that will contain the mean.")
    args = parser.parse_args()

    inputfile = args.inputfile
    setimages = np.loadtxt(inputfile, delimiter=' ', dtype='string')
    files = setimages[:, 0]
    
    mean = np.zeros((1, 3, 256, 256))
    for i, fname in enumerate(files, start=1):
        img = io.imread(fname)
        mean[0][0] += img[:, :, 0]
        mean[0][1] += img[:, :, 1]
        mean[0][2] += img[:, :, 2]
    mean[0] /= i

    blob = array_to_blobproto(mean)
    with open("{}.binaryproto".format(args.outputfile), 'wb') as f:
        f.write(blob.SerializeToString())
    np.save("{}.npy".format(args.outputfile), mean[0])

    meanimg = np.transpose(mean[0].astype(np.uint8), (1, 2, 0))
    io.imsave("{}.png".format(args.outputfile), meanimg)
