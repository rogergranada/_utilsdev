import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("3346.jpg")
image = image[:210,:]
"""
min_HSV = np.array([0, 58, 30], dtype = "uint8")
max_HSV = np.array([33, 150, 255], dtype = "uint8")
# Get pointer to video frames from primary device

imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
skinRegionHSV = cv2.inRange(imageHSV, min_HSV, max_HSV)
#image2 = np.ones(image.shape)*255

mask = cv2.bitwise_and(image, image, mask = skinRegionHSV)
#cv2.imwrite("283_s.jpg", np.hstack([image, mask]))

contours, hierarchy =  cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, contours, -1, (0, 0, 255), 3)

#cv2.imshow("Keypoints for ", im_with_keypoints)
#cv2.waitKey(0)  
"""
def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def findGreatesContour(contours):
    largest_area = 0
    largest_contour_index = -1
    i = 0
    total_contours = len(contours)
    while (i < total_contours ):
        area = cv2.contourArea(contours[i])
        if(area > largest_area):
            largest_area = area
            largest_contour_index = i
        i+=1
            
    return largest_area, largest_contour_index


hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
green_low = np.array([0, 58, 30] )
green_high = np.array([33, 150, 255])
curr_mask = cv2.inRange(hsv_img, green_low, green_high)
mask = cv2.bitwise_and(image, image, mask = curr_mask)
#viewImage(mask) ## 2
## contouring
RGB_again = cv2.cvtColor(mask, cv2.COLOR_HSV2RGB)
gray = cv2.cvtColor(RGB_again, cv2.COLOR_RGB2GRAY)
#viewImage(gray) ## 3
ret, threshold = cv2.threshold(gray, 75, 105, 0)
#viewImage(threshold) ## 4
contours, hierarchy =  cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
#viewImage(image) ## 5

max_contours = []
largest_area, largest_contour_index = findGreatesContour(contours)
max_contours.append(contours[largest_contour_index])
del contours[largest_contour_index]
largest_area, largest_contour_index = findGreatesContour(contours)
max_contours.append(contours[largest_contour_index])
cv2.drawContours(image, max_contours, -1, (0, 0, 255), 3)
viewImage(image)

