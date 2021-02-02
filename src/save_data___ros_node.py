#!/usr/bin/env python
import rospy
import time
from sorabot.msg import uvcontrol_msg

# Mario Soranno

uvcon = 0
uvcon_last = 0

def callback_receive_data(msg):
	global uvcon
	global uvcon_last
	
	uvcon = msg.on
	if uvcon != uvcon_last:
		uvcon_last = uvcon
		fileswitch = open("switchlamps.txt", "a")
		if uvcon == 1:
			now = time.strftime("%d/%m/%Y %H:%M:%S")
			text = now + " - ON\n"
			fileswitch.write(text)
		else:
			now = time.strftime("%d/%m/%Y %H:%M:%S")
			text = now + " - OFF\n"
			fileswitch.write(text)
		fileswitch.close()

if __name__ == '__main__':
	rospy.init_node('savedata')
	sub = rospy.Subscriber("uvcontrol", uvcontrol_msg, callback_receive_data)
	rospy.spin()