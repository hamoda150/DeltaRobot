import RPi.GPIO as GPIO     # Importing RPi library to use the GPIO pins
import time      # Importing sleep from time library to add delay in code
import math
    
def Servo_Init():
    servo_pin1 = 17      # Initializing the GPIO 17 for Rotate_Grip
    servo_pin2 = 27      # Initializing the GPIO 27 for Grip

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)          # We are using the BCM pin numbering
    GPIO.cleanup()
    GPIO.setup(servo_pin1, GPIO.OUT)     # Declaring GPIO 17 as output pin
    GPIO.setup(servo_pin2, GPIO.OUT)     # Declaring GPIO 27 as output pin

    global Rotate_Grip
    global Grip
    Rotate_Grip = GPIO.PWM(servo_pin1, 50)     # Created PWM channel at 50Hz frequency
    Grip = GPIO.PWM(servo_pin2, 50)     # Created PWM channel at 50Hz frequency
    Rotate_Grip.start(2.5)   
    Grip.start(2.5)                 

def Servo_map(theta): # input: 0-180 output:2.5-12.5
	# Linear equation to map beween angles and pulses
	pulse = (0.05555 * theta) + 2.5;
	return math.floor(pulse)

