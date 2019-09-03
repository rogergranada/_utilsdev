import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from os.path import splitext, basename, join, dirname

def find_hands_contour(contours, threshold=600):
    """ Identify contours by size of the area """
    hands_contours = []
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > threshold):
            hands_contours.append(contours[i])
    return hands_contours


def find_largest_contour(contours):
    """ Find the largest contour fo the list """
    largest_area = 0
    idx_largest = -1
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > largest_area):
            largest_area = area
            largest_contour_index = i
    return largest_area, idx_largest


def find_bounding_box(list_contours):
    """ Find minimum and maximum points for a single bbox """
    min_x, max_x = 256, 0 
    min_y, max_y = 256, 0
    for contour in list_contours:
        for points in contour:
            for x, y in points:
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
    return min_x, max_x, min_y, max_y 


def convert_xy_bbox(xmin, xmax, ymin, ymax):
    """ Convert x and y coordinates to x, y, w, and h """
    x = xmin-5 if (xmin > 5) else 0
    y = ymin-5 if (ymin > 5) else 0
    w = xmax-xmin+10 if (xmin > 5) else xmax-xmin
    h = ymax-ymin+10 if (ymin > 5) else ymax-ymin
    return x, y, w, h


def draw_box(image, bbox):
    """ Draw a bounding box in the input image """
    from PIL import Image
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np
    im = np.array(Image.open(image), dtype=np.uint8)
    fig, ax = plt.subplots(1)
    ax.imshow(im)
    for x, y, w, h in bbox:
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    plt.show()
    

def detect_skin(image):
    """ Detect hands by skin color """
    xmin, xmax, ymin, ymax = 0, 0, 0, 0
    image = image[:210,:]
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    skin_low = np.array([0, 58, 30] )
    skin_high = np.array([33, 150, 255])
    mask = cv2.inRange(hsv_img, skin_low, skin_high)
    mask = cv2.bitwise_and(image, image, mask=mask)

    rgb_mask = cv2.cvtColor(mask, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(rgb_mask, cv2.COLOR_RGB2GRAY)
    ret, threshold = cv2.threshold(gray, 75, 105, 0)
    contours, hierarchy = cv2.findContours(threshold, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE)
    hands = find_hands_contour(contours, threshold=600)
    if hands:
        xmin, xmax, ymin, ymax = find_bounding_box(hands)
    return xmin, xmax, ymin, ymax


def detect_person(image):
    """ Detect person by black t-shirt """
    xmin, xmax, ymin, ymax = 0, 0, 0, 0
    image = image[40:60,:]
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    person_low = np.array([0,0,100] )
    person_high = np.array([255,255,255])
    mask = cv2.inRange(hsv_img, person_low, person_high)
    mask = cv2.bitwise_and(image, image, mask=mask)
    mask = 255 - mask
    mask = np.uint8(np.where(mask > 200, 255, 0))
    rgb_mask = cv2.cvtColor(mask, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(rgb_mask, cv2.COLOR_RGB2GRAY)
    contours, hierarchy =  cv2.findContours(gray, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE)
    largest_area, largest_contour_index = find_largest_contour(contours)
    if largest_area:
        person = contours[largest_contour_index]
        xmin, xmax, _, _ = find_bounding_box([person])
        ymin, ymax = 0, 105
    return xmin, xmax, ymin, ymax


def detect_bbox_person(input_image):
    """ Given an image, detect the person and his hands to draw a box """
    image = cv2.imread(input_image)
    xmin_h, xmax_h, ymin_h, ymax_h = detect_skin(image)
    xmin_p, xmax_p, ymin_p, ymax_p = detect_person(image)
    xmin = xmin_h if (xmin_h < xmin_p) else xmin_p
    xmax = xmax_h if (xmax_h > xmax_p) else xmax_p
    ymin = ymin_h if (ymin_h < ymin_p) else ymin_p
    ymax = ymax_h if (ymax_h > ymax_p) else ymax_p
    x, y, w, h = convert_xy_bbox(xmin, xmax, ymin, ymax)
    #draw_box(input_image, [[x, y, w, h]])
    return x, y, w, h


def detect_from_file(inputfile, outputfile=None):
    """ Detect bounding boxes for a list of images in a file """
    if not outputfile:
        outputfile = join(dirname(inputfile), 'bbox_person.txt')
    with open(inputfile) as fin, open(outputfile, 'w') as fout:
        fout.write('Frame:\tLabel:\tPoints:\tBounding Box ID:\tFrame path:\n')
        for line in fin:
            path = line.strip()
            fname, _ = splitext(basename(path))
            x, y, w, h = detect_bbox_person(path)
            if not w and not h:
                fout.write('%s\tNone\t(-,-,-,-)\tNone\tNone\n' % fname)
            else:
                fout.write('%s\tperson\t(%d,%d,%d,%d)\t0\t%s\n' % (fname, x, y, w, h, path))


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('inputfile', metavar='txtfile', help='Path to the file containing paths for images')
    argparser.add_argument('-o', '--output', help='Path to the output file')
    args = argparser.parse_args()
    detect_from_file(args.inputfile, args.output)
