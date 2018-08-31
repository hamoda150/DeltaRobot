import numpy as np
import Kinematic_Get_theta

def IK(X0,Y0,Z0):
	theta1_global = Kinematic_Get_theta.Theta(X0,Y0,Z0)
	theta2_global = Kinematic_Get_theta.Theta(X0*np.cos(np.deg2rad(120)) + Y0*np.sin(np.deg2rad(120)), Y0*np.cos(np.deg2rad(120))-X0*np.sin(np.deg2rad(120)), Z0)
	theta3_global = Kinematic_Get_theta.Theta(X0*np.cos(np.deg2rad(120)) - Y0*np.sin(np.deg2rad(120)), Y0*np.cos(np.deg2rad(120))+X0*np.sin(np.deg2rad(120)), Z0)
	
	return theta1_global , theta2_global , theta3_global
