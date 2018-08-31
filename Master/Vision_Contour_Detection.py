import cv2
import numpy as np


def Contour_Detector(img):
    ############################################
    #              Image processing            # 
    ############################################
    # convert from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define the lower and upper boundaries of the "blue"
    Lower = (0, 228, 129)#(0, 0, 107)
    Upper = (33, 255, 255)#(74,255,255)
    # construct a mask for molto color, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    # cv2.inRange: Checks if array elements lie between the elements of two other arrays then return array contain array elements of 255 pixels (white) represents the tracked object
    mask = cv2.inRange(hsv, Lower, Upper)
    # Dilates an image: img, kernel used for erosion, number of times dilation is applied
 #   mask = cv2.dilate(mask, None, iterations=1)
    # Closing using 5x5 kernel
    kernel = np.ones((3,3),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    ############################################
    #          find contours in the mask       #
    ############################################
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)[-2]
 
    accepted_cnts = [0]
    # if there are no cnts return null
    if not cnts:
        pass
    else:
        for single_cnt in cnts:
           if is_contour_good(single_cnt):
                # append all good contours to cnts list
                accepted_cnts.append(single_cnt)

    # delete the first element of the list (its used only for declaring the list)
    del accepted_cnts[0]
    return accepted_cnts


# check if the contour has enough area: return true if the contour is bad
def is_contour_good(cnt):
    # the contour is 'bad' if it is hasn't enough area
    return (cv2.contourArea(cnt) > 1000)
