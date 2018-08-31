import math

def FK(theta1,theta2,theta3):
	# robot geometry
	# (look at pics above for explanation)
	e = 70.0       # end effector 72.59
	f = 115.0      # base 140.51
	re = 340.0     #426.8
	rf = 180.0     #180.0
	 
	# trigonometric constants
	sqrt3 = math.sqrt(3.0)
	pi = 3.141592653    # PI
	sin120 = sqrt3/2.0   
	cos120 = -0.5        
	tan60 = sqrt3
	sin30 = 0.5
	tan30 = 1/sqrt3
	 
	# FK
	t = (f-e)*tan30/2
	dtr = pi/180.0
	 
	theta1 = theta1 * dtr
	theta2 = theta2 * dtr
	theta3 = theta3 * dtr
	 
	y1 = -(t + rf*math.cos(theta1))
	z1 = -rf*math.sin(theta1)
	 
	y2 = (t + rf*math.cos(theta2))*sin30
	x2 = y2*tan60
	z2 = -rf*math.sin(theta2)
	 
	y3 = (t + rf*math.cos(theta3))*sin30
	x3 = -y3*tan60
	z3 = -rf*math.sin(theta3)
	 
	dnm = (y2-y1)*x3-(y3-y1)*x2
	 
	w1 = y1*y1 + z1*z1
	w2 = x2*x2 + y2*y2 + z2*z2
	w3 = x3*x3 + y3*y3 + z3*z3
	     
	# x = (a1*z + b1)/dnm
	a1 = (z2-z1)*(y3-y1)-(z3-z1)*(y2-y1)
	b1 = -((w2-w1)*(y3-y1)-(w3-w1)*(y2-y1))/2.0
	 
	# y = (a2*z + b2)/dnm
	a2 = -(z2-z1)*x3+(z3-z1)*x2
	b2 = ((w2-w1)*x3 - (w3-w1)*x2)/2.0
	 
	# a*z^2 + b*z + c = 0
	a = a1*a1 + a2*a2 + dnm*dnm
	b = 2*(a1*b1 + a2*(b2-y1*dnm) - z1*dnm*dnm)
	c = (b2-y1*dnm)*(b2-y1*dnm) + b1*b1 + dnm*dnm*(z1*z1 - re*re)
	  
	# discriminant
	d = b*b - 4.0*a*c
	if (d < 0): # non-existing point
		print("non-existing point")

	Z0_global = -0.5*(b+math.sqrt(d))/a
	X0_global = (a1*Z0_global + b1)/dnm
	Y0_global = (a2*Z0_global + b2)/dnm

	return X0_global , Y0_global , Z0_global
	
