#!/usr/bin/env python
import rospy
import RPi.GPIO as GPIO
from sorabot.msg import drivers_msg

# Mario Soranno

def callback_receive_data(msg):
	if msg.direction == 0:
		GPIO.output(7, GPIO.LOW)
		GPIO.output(11, GPIO.LOW)	
	else:
		GPIO.output(7, GPIO.HIGH)
		GPIO.output(11, GPIO.HIGH)	
	
	if msg.rotation == 1:
		pwm_left.start(msg.velocity)
		pwm_right.start(msg.velocity+10)
	elif msg.rotation == 3:
		pwm_left.start(msg.velocity+10)
		pwm_right.start(msg.velocity)
	else:	# 2	
		pwm_left.start(msg.velocity)
		pwm_right.start(msg.velocity)
	
if __name__ == '__main__':
	rospy.init_node('drivers')
	sub = rospy.Subscriber("drivers", drivers_msg, callback_receive_data)
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)	# This example uses the BOARD pin numbering
	GPIO.setup(12, GPIO.OUT)
	GPIO.setup(33, GPIO.OUT)
	GPIO.setup(7, GPIO.OUT)
	GPIO.setup(11, GPIO.OUT)
	pwm_left = GPIO.PWM(12, 5000)
	pwm_right = GPIO.PWM(33, 5000)	
	rospy.spin()
pwm_left.stop()
pwm_left.stop()