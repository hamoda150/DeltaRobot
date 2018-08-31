import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab
import Contour_Detection


while(True):
    # Capture frame by frame from LabTop screen [frame size:450x540]
    frame =  np.array(ImageGrab.grab(bbox=(130,50,670,500)))
    #invert color from B,G,R to R,G,B because we want to plot using matplotlib
    b,g,r = cv2.split(frame)      # get BGR values from the image
    frame = cv2.merge([r,g,b])    # store values as RGB
    # Draw rectangle: img, startPoint_lowerRightCorner, endPoint_upperLeftCorner, BGR color value, thickness of the line 3 px
    cv2.rectangle(frame,(363,447),(228,105),(0,255,0),3)
    # copy the desired part of the image: img[Y1:Y2, X1:X2]
    part = frame[105:447, 228:363]
    cv2.imshow("part", part)
    cv2.imshow("full", frame)

    # Find contours
    #cnts = Contour_Detection.Contour_Detector(frame)


    if(cv2.waitKey(1)&0xFF == ord('q')):
        break
cv2.destroyAllWindows()
