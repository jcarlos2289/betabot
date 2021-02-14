#!/usr/bin/env python
import rospy
from gpiozero import LineSensor
from betabot.msg import linefollower_msg

# Mario Soranno

if __name__ == '__main__':
	rospy.init_node('linefollower')
	pub = rospy.Publisher("/linefollower", linefollower_msg, queue_size = 10)
	rate = rospy.Rate(10)
	inc = 0
	followerSX = LineSensor(27)
	followerSXC = LineSensor(22)
	followerDXC = LineSensor(23)
	followerDX = LineSensor(24)
	while not rospy.is_shutdown():
		inc = inc + 1
		msg = linefollower_msg()
		msg.inc = inc
		
		if int(followerSX.value) == 0:
			msg.followerSX = 0
		else:
			msg.followerSX = 1
			
		if int(followerSXC.value) == 0:
			msg.followerSXC = 0
		else:
			msg.followerSXC = 1

		if int(followerDXC.value) == 0:
			msg.followerDXC = 0
		else:
			msg.followerDXC = 1
			
		if int(followerDX.value) == 0:
			msg.followerDX = 0
		else:
			msg.followerDX = 1
	
		pub.publish(msg)
		rate.sleep()
