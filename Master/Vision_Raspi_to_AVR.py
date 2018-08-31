# Mater SPI controlling 3 AVRs
# RPi PINOUTS
# MOSI -> GPIO10
# MISO -> GPIO9
# SCK  -> GPIO11
# CE1  -> GPIO0
# CE2  -> GPIO5
# CE3  -> GPIO6
# INT  -> GPIO2

# Multi slaves Tut: https://raspberrypi.stackexchange.com/questions/71448/how-to-connect-multiple-spi-devices-adcs-to-raspberry-pi/71504#71504
#    			  : http://www.takaitra.com/posts/492
#					https://stackoverflow.com/questions/3123371/splitting-a-16-bit-int-into-two-8-bit-ints-in-python

# Kinematics
import Kinematic_Forward
import Kinematic_Inverse
import Kinematic_Get_theta
import math
# SPI
import RPi.GPIO as GPIO
import serial
import time
import servo
#import Vision_system


# Serila config
ser = serial.Serial()
ser.port = '/dev/ttyS0'
ser.baudrate = 9600

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
Rotate_Grip.start(2.5)   
Grip.start(10.5)

# SPI initialization
# setup the pins as output and input as needed
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
Product_number = 0
Product_number_global = 0

def Counter(Product_number):
    global Product_number_global
    Product_number_global = Product_number
    return Product_number

def Send_to_Arduino(pulse1,pulse2,pulse3):
    global ser
    ser.open()
    # Stop conv belt
    ser.write(b'1')
    time.sleep(1.5)
    ser.write(str(pulse1))
    time.sleep(1.5)
    ser.write(str(pulse2))
    time.sleep(1.5)
    ser.write(str(pulse3))
    time.sleep(1.5)
    print('Data has been sent!')
    ser.close()


def Robot_Homing():
    global ser
    ser.open()
    # move conv belt
    ser.write(b'0')
    time.sleep(1.5)
    pulse1=0
    pulse2=0
    pulse3=0
    ser.write(str(pulse1))
    time.sleep(1.5)
    ser.write(str(pulse2))
    time.sleep(1.5)
    ser.write(str(pulse3))
    time.sleep(1.5)
    print('Data has been sent!')
    ser.close()

def Robot_intermediate():
    global ser
    ser.open()
    # stop conv belt
    ser.write(b'1')
    time.sleep(1.5)
    pulse1=0
    pulse2=0
    pulse3=0
    ser.write(str(pulse1))
    time.sleep(1.5)
    ser.write(str(pulse2))
    time.sleep(1.5)
    ser.write(str(pulse3))
    time.sleep(1.5)
    print('Data has been sent!')
    ser.close()

def Motor_map(theta):
	# Linear equation to map beween angles and pulses
	pulse = (13.75 * theta) + 650.2434;
	return math.floor(pulse)
    
def Position_Process(DISTANCE,ORIENTATION):
	# Proceed if the distance is 30cm from camera to the product
	if (DISTANCE > 50) and (DISTANCE < 55): #34-35
		#################################
		#	Orientation of the gripper	#
		#################################
		# gripp the product (gripper attached to Raspberry pi)
		# Rotate_Grip range: 10 or 180(45deg), 130(90deg), 50(180deg)
		# Grip range: 3(grip), 10.5(ungrip)
		if (ORIENTATION == 45):
		    Rotate_Grip.ChangeDutyCycle(servo.Servo_map(10))
		    #Grip.ChangeDutyCycle(3)
		if (ORIENTATION == 90):
		    Rotate_Grip.ChangeDutyCycle(10.5)#Rotate_Grip.ChangeDutyCycle(servo.Servo_map(130))
		    #Grip.ChangeDutyCycle(3)
		if (ORIENTATION == 180):
		    Rotate_Grip.ChangeDutyCycle(6)
		    #Grip.ChangeDutyCycle(3)
		#################################
		#	Posision of the gripper	#
		#################################
		# Stop the belt, 1 means stop, 0 means start
		
		# required POS: (don't care, don't car, 54) (without gripper attached)
		# required POS: (don't car ,don't car ,67) (with gripper attached)
	#	pos = Kinematic_Forward.FK(55,90,55)
	#          Kinematic_Inverse.IK(X0,Y0,Z0)
		theta1 = int(Motor_map(74))#55
		theta2 = int(Motor_map(74))#90
		theta3 = int(Motor_map(74))#55
	#	Robot_intermediate()
		# Pick
		Send_to_Arduino(Motor_map(25),Motor_map(25),Motor_map(25))
		Send_to_Arduino(theta1,theta2,theta3)
		time.sleep(1)
                Grip.ChangeDutyCycle(3)
                # Place
		Send_to_Arduino(int(Motor_map(0)),int(Motor_map(100)),int(Motor_map(90)))
		time.sleep(1)
		Grip.ChangeDutyCycle(7)
		Product_number = Product_number + 1
                Counter(Product_number)
	else:
		pass #Robot_Homing()



'''
    Grip.ChangeDutyCycle(2.5)
    Rotate_Grip.ChangeDutyCycle(servo.Servo_map(0))



theta1 = int(Motor_map(90))
theta2 = int(Motor_map(90))
theta3 = int(Motor_map(90))
Send_to_Arduino(theta1,theta2,theta3)

Robot_Homing()

theta1 = int(Motor_map(0))
theta2 = int(Motor_map(0))
theta3 = int(Motor_map(0))
Send_to_AVR1(theta1,theta2)
Send_to_AVR2(theta3)
time.sleep(3)
  
theta1 = int(Motor_map(90))
theta2 = int(Motor_map(90))
theta3 = int(Motor_map(90))
Send_to_AVR1(theta1,theta2)
Send_to_AVR2(theta3)
time.sleep(3)
'''
