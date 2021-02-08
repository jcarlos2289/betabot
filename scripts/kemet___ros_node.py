#!/usr/bin/env python
import rospy
import serial
from sorabot.msg import kemet_msg

# Mario Soranno

port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)

def readlineCR(port):
    rv = ""
    while True:
		ch = port.read()
		if ch != '\n':
			rv += ch
			if ch=='\r' or ch=='':
				return rv

if __name__ == '__main__':
	rospy.init_node('kemet')
	pub = rospy.Publisher("/kemet", kemet_msg, queue_size = 10)
	rate = rospy.Rate(10)
	inc = 0
	kemetF = 0
	kemetB = 0
	while not rospy.is_shutdown():	
		rcv = readlineCR(port)
		numelement = len(rcv)		
		msg = kemet_msg()
		inc = inc + 1
		msg.inc = inc
		if numelement == 5:
			msg.kemetF = int(rcv[1])
			msg.kemetB = int(rcv[3])
		else:
			msg.kemetF = 0
			msg.kemetB = 0
		
		pub.publish(msg)
		rate.sleep()