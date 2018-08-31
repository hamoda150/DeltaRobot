import cv2
import numpy as np
import Contour_Detection
import Distance

def Camera_calibration():
	# initialize the known distance from the camera to the object, which
	# in this case is 24 inches
	KNOWN_DISTANCE = 41.0

	# initialize the known object width, which in this case, the piece of
	# paper is 12 inches wide
	KNOWN_WIDTH = 3.5 # 3.5x6 cm

	# initialize the list of images that we'll be using
	IMAGE_PATHS = ["images/100.jpg", "images/80.jpg", "images/50.jpg"]

	# load the furst image that contains an object that is KNOWN TO BE 2 feet
	# from our camera, then find the paper marker in the image, and initialize
	# the focal length
	image = cv2.imread("image/molto.jpg")
	accepted_cnts = Contour_Detection.Contour_Detector(image)
	rect = cv2.minAreaRect(accepted_cnts[0])
	focalLength = (rect[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
	return focalLength
