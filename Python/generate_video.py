import cv2
import numpy as np
import glob
import argparse
from os.path import join, basename, dirname, splitext

def main(inputfile, outputfile):
    if not outputfile:
        fname, _ = splitext(basename(inputfile))
        outputfile = join(dirname(inputfile), fname+'.avi')

    images = []
    print('Loading images')
    with open(inputfile) as fin:
        for line in fin:
            filename = line.strip().split()[0]
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            images.append(img)

    print('Saving images in video')
    out = cv2.VideoWriter(outputfile, cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    for i in range(len(images)):
        out.write(images[i])
    out.release()
    print('Recorded {} frames.'.format(i))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('inputfile', metavar='input_file', help='File containing paths to images')
    argparser.add_argument('-o', '--output', help='Path to the output file', default=None)
    args = argparser.parse_args()
    main(args.inputfile, args.output)

