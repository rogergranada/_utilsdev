import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"],0)
edges = cv2.Canny(img,10,350)

cv2.imshow("Output", edges)
cv2.waitKey(0)

