# USAGE
# run the function Camera_calibration() separately to get focalLength
import numpy as np
import cv2
import Vision_Contour_Detection

########################################
#   find the distance from the camera  #
######################################## 
def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

#################################################
#   Camera calibration for the first time only  #
################################################# 
def Camera_calibration():
	# initialize the known distance from the camera to the object, which
	# in this case is 24 cm
	KNOWN_DISTANCE = 41.5

	# initialize the known object width, which in this case, the piece of
	# paper is 12 inches wide
	KNOWN_WIDTH = 3.5 # 3.5x6 cm

	# initialize the list of images that we'll be using
	IMAGE_PATHS = ["images/100.jpg", "images/80.jpg", "images/50.jpg"]

	# load the furst image that contains an object that is KNOWN TO BE 2 feet
	# from our camera, then find the paper marker in the image, and initialize
	# the focal length
	image = cv2.imread("part.jpg")
	accepted_cnts = Vision_Contour_Detection.Contour_Detector(image)
	rect = cv2.minAreaRect(accepted_cnts[0])
	focalLength = (rect[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
	return focalLength

###########################
#   loop over the images  #
###########################

def find_distance(rect,focalLength,KNOWN_WIDTH,display):
	cm = distance_to_camera(KNOWN_WIDTH, focalLength, rect[1][0])
	# draw a bounding box around the image and display it
	box = np.int0(cv2.boxPoints(rect))
	#cv2.drawContours(display, [box], -1, (255, 0, 0), 2)
	return cm
#	cv2.putText(display, "%.2fcm" % (cm),
#		(display.shape[1] - 200, display.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
#		2.0, (0, 255, 0), 3)
