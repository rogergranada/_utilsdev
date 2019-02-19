#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
Having two maps, a correct oriented map and a non-oriented map, align the latter using the
orientation of the former. In order to do so, we use ORB to detect features and Homography, 
i.e, a 3x3 matrix transformation, to map the points in one image to the corresponding 
points in the other image. 
"""

import argparse
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import cv2
import numpy as np
from os.path import realpath, join, basename, splitext, dirname


def align_images(image, goldimg, max_feats=300, max_percent=0.5):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_goldimg = cv2.cvtColor(goldimg, cv2.COLOR_BGR2GRAY)
   
    # Use ORB to detect features
    orb = cv2.ORB_create(max_feats)
    keypts_image, desc_image = orb.detectAndCompute(gray_image, None)
    keypts_goldimg, desc_goldimg = orb.detectAndCompute(gray_goldimg, None)
   
    # Match features
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(desc_image, desc_goldimg, None)
   
    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)
 
    # Remove not so good matches
    nb_matches = int(len(matches) * max_percent)
    matches = matches[:nb_matches]
 
    # Draw top matches
    img_matches = cv2.drawMatches(image, keypts_image, goldimg, keypts_goldimg, matches, None)
   
    # Extract location of good matches
    points_image = np.zeros((len(matches), 2), dtype=np.float32)
    points_goldimg = np.zeros((len(matches), 2), dtype=np.float32)
 
    for i, match in enumerate(matches):
        points_image[i, :] = keypts_image[match.queryIdx].pt
        points_goldimg[i, :] = keypts_goldimg[match.trainIdx].pt
   
    # Find homography
    h, mask = cv2.findHomography(points_image, points_goldimg, cv2.RANSAC)
 
    # Use homography
    height, width, channels = goldimg.shape
    aligned = cv2.warpPerspective(image, h, (width, height), borderValue=(205, 205, 205))
    return aligned, h, img_matches


def main(mapgold, imgmap, folderout, maxfeats, percentmatch):
    mapgold = realpath(mapgold)
    imgmap = realpath(imgmap)
    folderout = realpath(folderout)    

    goldmap = cv2.imread(mapgold)
    imagemap  = cv2.imread(imgmap)
    
    alignedmap, h, img_matches = align_images(imagemap, goldmap, max_feats=maxfeats, max_percent=percentmatch)

    # Save matches image
    outfile = join(folderout, "matches.png")
    logger.info("Saving matches image : %s" % outfile) 
    cv2.imwrite(outfile, img_matches)

    # Save aligned image
    outfile = join(folderout, "aligned.png")
    logger.info("Saving aligned image : %s" % outfile) 
    cv2.imwrite(outfile, alignedmap)

    # Print estimated homography
    logger.info("Estimated homography :")
    logger.info(h)
    with open(join(folderout, "homography.txt"), 'w') as fout:
        fout.write('%r' % h)


if __name__ == "__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument('goldmap', metavar='mapfile', help='Map with the correct orientation.')
    parser.add_argument('imagemap', metavar='imgfile', help='Map with the orientation to be fixed.')
    parser.add_argument('output_folder', metavar='folder_out', help='Folder to save files.')
    parser.add_argument('-m', '--maxfeats', help='Number maximum of features', default=300, type=int)
    parser.add_argument('-p', '--percentmatch', help='Percentage of good features', default=0.5)
    args = parser.parse_args()
    main(args.goldmap, args.imagemap, args.output_folder, args.maxfeats, args.percentmatch)
