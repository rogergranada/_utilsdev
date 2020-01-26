#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, argparse
import shutil, os, glob
from os import listdir
from os.path import realpath, isdir, isfile, join, splitext


def main(folder):
    folder = realpath(folder)
    if not isdir(folder):
        print 'Path %s is not a folder' % folder
        sys.exit(0)

    dfolder = {}
    for f in listdir(folder):
        if isfile(join(folder, f)):
            fname, ext = splitext(f)
            if ext == '.jpg':
                dirin = fname.split('_')[0]
                dfolder[dirin] = ''

    for d in sorted(dfolder):
        dirout = join(folder, d)
        if isdir(dirout):
            print 'Folder %s already exists' % dirout
            print 'Not moving files into the folder'
        else:
            os.mkdir(dirout)
            print 'Moving '+folder+'/'+d+'_*.jpg to '+dirout
            mvfiles = glob.glob(folder+'/'+d+'_*.jpg')
            for f in mvfiles:
                shutil.move(f, dirout)
    
    print 'Finished moving files!'



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfolder', metavar='folder_input', help='folder containing images')
    args = parser.parse_args()

    main(args.inputfolder)
