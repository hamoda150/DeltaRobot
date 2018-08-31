# Computer Vision
# video capture: 
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video import VideoStream
import imutils
import time
import Vision_Contour_Detection
import Vision_Distance
import Vision_Raspi_to_AVR
import servo
import RPi.GPIO as GPIO

GPIO.cleanup()
# servo config
servo_pin1 = 17      # Initializing the GPIO 17 for Rotate_Grip
servo_pin2 = 27      # Initializing the GPIO 27 for Grip
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)          # We are using the BCM pin numbering
GPIO.setup(servo_pin1, GPIO.OUT)     # Declaring GPIO 17 as output pin
GPIO.setup(servo_pin2, GPIO.OUT)     # Declaring GPIO 27 as output pin
Rotate_Grip = GPIO.PWM(servo_pin1, 50)     # Created PWM channel at 50Hz frequency
Grip = GPIO.PWM(servo_pin2, 50)     # Created PWM channel at 50Hz frequency
#global Rotate_Grip
#global Grip
Rotate_Grip.start(6)   
Grip.start(3)

# Robot Home Position
Vision_Raspi_to_AVR.Robot_Homing()
# Grip home position
Grip.ChangeDutyCycle(7)


# Calibrating Camera and getting focal length
focalLength = 408.491968972 #500.02557809#1224.30644008             #598.12060547                    # func:386.57142857142856 # tut:543.458329634233
KNOWN_WIDTH = 3.5 # 3.5x6 cm
IMAGE_PATHS = ["images/100.jpg", "images/80.jpg", "images/50.jpg"]
#print(Vision_Distance.Camera_calibration())


# Are we using the Pi Camera?
usingPiCamera = True
# Set initial frame size.
frameSize = (450, 540)
 
# Initialize mutithreading the video stream.
vs = VideoStream(src=0, usePiCamera=usingPiCamera, resolution=frameSize,
		framerate=32).start()
# Allow the camera to warm up.
time.sleep(2.0)

#counter = 0 # to process limited number of frames
Product_number = 0

    
# capture frames from the camera
while True:
    # Get the next frame.
    frame = vs.read()
    
    # If using a webcam instead of the Pi Camera,
    # we take the extra step to change frame size.
    if not usingPiCamera:
	frame = imutils.resize(frame, width=frameSize[0])
    # Draw rectangle: img, startPoint_lowerRightCorner, endPoint_upperLeftCorner, BGR color value, thickness of the line 3 px
 #   cv2.rectangle(frame,(363,447),(228,105),(0,255,0),3)
    # copy the desired part of the image (ROI): img[Y1:Y2, X1:X2]
    part = frame[150:450, 190:350]
    display = part
 #   cv2.imshow("frame", frame)

    # Find contours in the part
    accepted_cnts = Vision_Contour_Detection.Contour_Detector(part)

    #####################################
    #       find contours' centers      #
    #####################################
    # Image moments if there are contours only. M is a dictionary
    if accepted_cnts:
        cx = [0]     # list to hold x-positions
        cy = [0]     # list to hold y-positions
        for index in range(len(accepted_cnts)):   
            M = cv2.moments(accepted_cnts[index]) 
            # [1] Centroid is given by the relations. need explict type casting to int to perform math operations
            cx.append(int(M['m10']/M['m00']))
            cy.append(int(M['m01']/M['m00']))
            # put dot in the center of the contour
            # Draw circle: img, center, radius, BGR color value, thickness of the line
            cv2.circle(display,(cx[index+1],cy[index+1]), 5, (255,0,0), -1)
            # compare contours' centers with action region
            if (cy[index+1] > 20) and (cy[index+1] < 250):
                # take action 1
  #              print("Action 1 !")
                #################################
                #   end-effector orientation    #
                #################################
                #  returns the rotated rectangle in which the ellipse is inscribed (Return top-left corner(x,y), (width, height), angle of rotation)
                (x,y),(MA,ma),angle = cv2.fitEllipse(accepted_cnts[index])
                if angle > 90:
                    angle = 180 - angle
                if (angle > 0) and (angle < 15):
                    print("90 deg grip")
                    ORIENTATION = 90
                if (angle >= 15) and (angle < 60):
                    print("45 deg grip")
                    ORIENTATION = 45
                if (angle >= 60) and (angle <= 180):
                    print("180 deg grip")
                    ORIENTATION = 180
                print(ORIENTATION)
                # Send command to the servo motor of the gripper

                ###################################
                #       end-effector position     #
                ###################################
                # draw bounding rectagle
                # Return top-left corner(x,y), (width, height), angle of rotation
                rect = cv2.minAreaRect(accepted_cnts[index])
                # Returns 4 points to draw the rectangle
                box = cv2.boxPoints(rect)
                # round the values to nearest integer.
                box = np.int0(box)
                cv2.drawContours(display,[box],0,(0,255,0),2)
                # find Distance and print it
                cm = Vision_Distance.find_distance(rect,focalLength,KNOWN_WIDTH,display)
                # offset error by 8
                print(cm)
                DISTANCE = cm
                # Send command to the servo motor of the gripper
                #Vision_Raspi_to_AVR
             #   counter = counter + 1
             #   if(counter == 20):
              Vision_Raspi_to_AVR.Position_Process(DISTANCE,ORIENTATION)
            else:
                print("Out of range!")
    else:
        cx = [0]
        cy = [0]


    
    #####################################################
    #   Draw a red line indicating the action region    #
    #####################################################
    #: img, startPoint, endPoint, BGR color value, thickness of the line 5 px
    cv2.line(frame, (0,150), (450,150), (0,0,255), 5)
    cv2.line(frame, (0,450), (450,450), (0,0,255), 5)

    cv2.imshow("frame", frame)
    cv2.imshow("display", display)
    Product_number = Vision_Raspi_to_AVR.Counter()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'Number of Products: '+str(Product_number),(20,30), font, 1,(255,255,255),2,cv2.LINE_AA)
    # calculate contour area and exclode corrupted products (action 2)

   
    if(cv2.waitKey(1)&0xFF == ord('q')):
        break
cv2.destroyAllWindows()
vs.stop()


'''
def system_Grip(value):
    Grip.ChangeDutyCycle(value)
 
def system_Rotate_Grip(value):
    Rotate_Grip.ChangeDutyCycle(servo.Servo_map(value))
'''    
    