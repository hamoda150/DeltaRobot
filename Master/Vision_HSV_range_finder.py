import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

#cap = cv2.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
h_lower,s_lower,v_lower = 100,100,100
h_upper,s_upper,v_upper = 100,100,100

# Creating track bar for lower limit
cv2.createTrackbar('h_lower', 'result',0,179,nothing)
cv2.createTrackbar('s_lower', 'result',0,255,nothing)
cv2.createTrackbar('v_lower', 'result',0,255,nothing)

# Creating track bar for upper limit
cv2.createTrackbar('h_upper', 'result',0,179,nothing)
cv2.createTrackbar('s_upper', 'result',0,255,nothing)
cv2.createTrackbar('v_upper', 'result',0,255,nothing)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (700,350)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(700,350))
# allow the camera to warmup
time.sleep(0.1)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):  
    image = frame.array
    # Resize the images, 750X600 sound cool
    #image = cv2.resize(image,(700,350))
    #converting to HSV
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h_lower = cv2.getTrackbarPos('h_lower','result')
    s_lower = cv2.getTrackbarPos('s_lower','result')
    v_lower = cv2.getTrackbarPos('v_lower','result')
    
    # get info from track bar and appy to result
    h_upper = cv2.getTrackbarPos('h_upper','result')
    s_upper = cv2.getTrackbarPos('s_upper','result')
    v_upper = cv2.getTrackbarPos('v_upper','result')

    # Normal masking algorithm
    lower_limit = np.array([h_lower,s_lower,v_lower])
    upper_limit = np.array([h_upper,s_upper,v_upper])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv,lower_limit, upper_limit)
    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image,image,mask = mask)

    cv2.imshow('result',result)
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
	
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

#cap.release()

cv2.destroyAllWindows()
