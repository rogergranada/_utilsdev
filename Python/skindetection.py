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
    x = xmin-10 if (xmin > 10) else 0
    y = ymin-10 if (ymin > 10) else 0
    w = xmax-xmin+20 if (xmin > 10) else xmax-xmin
    h = ymax-ymin+20 if (ymin > 10) else ymax-ymin
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
    image = image[:130,:]
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    skin_low = np.array([0, 48, 80], dtype = "uint8")
    skin_high = np.array([20, 255, 255], dtype = "uint8")
    mask = cv2.inRange(hsv_img, skin_low, skin_high)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skinMask = cv2.erode(mask, kernel, iterations=2)
    skinMask = cv2.dilate(skinMask, kernel, iterations=2)
    
    xmin, xmax, ymin, ymax = 256, 0, 0, 0
    for i in range(skinMask.shape[0]):
        pix_person = np.nonzero(skinMask[i] == 255)[0]
        if len(pix_person) != 0:
            xmin_line = np.min(pix_person)
            xmax_line = np.max(pix_person)
            ymax = i
            if xmin_line < xmin: xmin = xmin_line
            if xmax_line > xmax: xmax = xmax_line
    w = xmax-xmin+20
    h = ymax+10
    return xmin, 0, w, h
    

def detect_skin_old(image):
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
    
    arr = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(arr) == 2:
        contours, hierarchy = arr
        hands = find_hands_contour(contours, threshold=800)
        if hands:
            xmin, xmax, ymin, ymax = find_bounding_box(hands)
    #cv2.imshow('None', mask)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return xmin, xmax, ymin, ymax


def detect_person(image):
    grayscaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, im_thr = cv2.threshold(grayscaled[5:100,:], 125, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernel = np.ones((5,5), np.uint8)
    im_thr = cv2.dilate(im_thr, kernel, iterations=2)
    xmin, xmax = 256, 0

    for i in range(im_thr.shape[0]):
        pix_person = np.nonzero(im_thr[i] == 0)
        if len(pix_person[0]) != 0:
            xmin_line = np.min(pix_person)
            xmax_line = np.max(pix_person)
            if xmax_line > xmax: xmax = xmax_line
            if xmin_line < xmin: xmin = xmin_line
    x = xmin-10
    y = 0
    w = xmax-xmin+20
    h = 114
    plt.imshow(im_thr, cmap='gray')
    plt.show()
    return x, y, w, h


def detect_person_old(input_image):
    """ Detect person by black t-shirt """
    image = cv2.imread(input_image)
    xmin, xmax, ymin, ymax = 0, 0, 0, 0
    image = image[:60,:]
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    person_low = np.array([0,0,100] )
    person_high = np.array([255,255,255])
    mask = cv2.inRange(hsv_img, person_low, person_high)
    mask = cv2.bitwise_and(image, image, mask=mask)
    mask = 255 - mask
    mask = np.uint8(np.where(mask > 200, 255, 0))
    rgb_mask = cv2.cvtColor(mask, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(rgb_mask, cv2.COLOR_RGB2GRAY)
    arr = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(arr) == 2:
        contours, hierarchy = arr
        largest_area, largest_contour_index = find_largest_contour(contours)
        if largest_area:
            person = contours[largest_contour_index]
            xmin, xmax, _, _ = find_bounding_box([person])
            ymin, ymax = 0, 114
    #cv2.imshow('None', mask)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return xmin, xmax, ymin, ymax

def fix_coordinates(x, y, w, h):
    if x < 0:
        w -= x
        x = 0
    if y < 0:
        h -= y
        y = 0
    if x+w > 257:
        w = 257-x
    if y+h > 257:
        h = 257-y
    return x, y, w, h


def detect_bbox_person(input_image):
    """ Given an image, detect the person and his hands to draw a box """
    xmin_h, ymin_h, w_h, h_h = detect_skin(input_image)
    xmin_p, ymin_p, w_p, h_p = detect_person(input_image)
    x = xmin_h if (xmin_h < xmin_p) else xmin_p
    y = 0
    if w_h > w_p:
        w = w_h
    else:
        w = w_p
    wn = w_h if (w_h > w_p) else w_p
    print w, wn
    h = h_h if (h_h > h_p) else h_p
    x, y, w, h = fix_coordinates(x, y, w, h)
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
            if not w:
                fout.write('%s\tNone\t(-,-,-,-)\tNone\tNone\n' % fname)
            else:
                fout.write('%s\tperson\t(%d,%d,%d,%d)\t0\t%s\n' % (fname, x, y, w, h, path))


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('inputfile', metavar='txtfile', help='Path to the file containing paths for images')
    argparser.add_argument('-o', '--output', help='Path to the output file')
    args = argparser.parse_args()
    detect_from_file(args.inputfile, args.output)
