#!/usr/bin/python
#-*- coding: utf-8 -*-

import cv2
import os
from os.path import splitext, join, basename, dirname, isfile
import argparse
#from progressBar import ProgressBar

def getNamesAsInts(files_list):
    """
    Receive a list containing the filenames and return a list
    containing the numbers referring to the names.
    """
    fids = []
    for fname in files_list:
        name, ext = splitext(basename(fname))
        if ext == '.jpg':
            fids.append(int(name))
    return sorted(fids) 


def backgroundSubtraction(input, output_folder):
    """
    Receives a folder or a file containing images in jpg 
    format and remove the background for each image. 
    Files are saved in output_folder.

    Parameters:
    -----------
    input_folder : string
        path to the folder containing images
    output_folder : string
        path to the folder where images are saved.
    """
    if isfile(input):
        list_files = [line.strip() for line in open(input)]
    else:
        list_files = os.listdir(input)
    if list_files:
        rootname = dirname(list_files[0])
        files_ids = getNamesAsInts(list_files)

    #fgbg = cv2.createBackgroundSubtractorMOG2()
    fgbg = cv2.BackgroundSubtractorMOG()
    #pb = ProgressBar(len(files_ids))
    #train background subtractor :: about 50 images
    for id in files_ids[:50]:
        path_img = join(rootname, str(id)+'.jpg')
        img = cv2.imread(path_img, 1)
        fgbg.apply(img)

    #apply remotion of the background in all images
    for id in files_ids:
        path_img = join(rootname, str(id)+'.jpg')
        path_out = join(output_folder, str(id)+'.jpg')
        img = cv2.imread(path_img, 1)
        fgmask = fgbg.apply(img)
        cv2.imwrite(path_out, fgmask)
        #pb.update()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir', metavar='dir_input', help='folder containing input images.')
    parser.add_argument('outputdir', metavar='dir_output', help='folder to save output images')
    args = parser.parse_args()

    backgroundSubtraction(args.inputdir, args.outputdir)
