import numpy as np

def Theta(X0,Y0,Z0):
	# robot geometry
	# (look at pics above for explanation)
	e = 70.0       # end effector 72.59
	f = 115.0      # base 140.51
	re = 340.0     #426.8
	rf = 180.0     #180.0
	 
	# trigonometric constants
	sqrt3 = np.sqrt(3.0)
	pi = 3.141592653    # PI
	sin120 = sqrt3/2.0   
	cos120 = -0.5        
	tan60 = sqrt3
	sin30 = 0.5
	tan30 = 1/sqrt3


	# Getting theta
	y1 = -0.5 * 0.57735 * f    # f/2 * tg 30
	Y0 = Y0 - (0.5 * 0.57735 * e)    # shift center to edge

	# z = a + b*y
	a = (X0*X0 + Y0*Y0 + Z0*Z0 +rf*rf - re*re - y1*y1)/(2*Z0)
	b = (y1-Y0)/Z0
	# discriminant
	d = -(a+b*y1)*(a+b*y1)+rf*(b*b*rf+rf) 
	if (d < 0):  # non-existing point
		print("non-existing point")
	     
	yj = (y1 - a*b - np.sqrt(d))/(b*b + 1) # choosing outer point
	zj = a + b*yj
	if(yj>y1):
		value = 180.0 
	else:
		value = 0.0
	theta = 180.0*np.arctan(-zj/(y1 - yj))/pi + value

	return theta
