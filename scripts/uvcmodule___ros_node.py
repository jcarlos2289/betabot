#!/usr/bin/env python
import rospy
import serial
from std_msgs.msg import Int8
from sorabot.msg import uvcontrol_msg

# Mario Soranno

ser = serial.Serial("/dev/ttyUVC", baudrate=9600, timeout=3.0)

def callback_receive_data(msgrec):
	if msgrec.horizontal == 1 and msgrec.on == 1:
		ser.write('1')
	elif msgrec.horizontal == 0 and msgrec.on == 1:
		ser.write('0')
	else:
		ser.write('2')

def readlineCR(ser):
    rv = ""
    while True:
		ch = ser.read()
		if ch != '\n':
			rv += ch
			if ch=='\r' or ch=='':
				return rv

if __name__ == '__main__':
	rospy.init_node('uvcmodule')
	pub = rospy.Publisher("uvcvalue", Int8, queue_size = 10)
	sub = rospy.Subscriber("uvcontrol", uvcontrol_msg, callback_receive_data)	
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():	
		rcv = readlineCR(ser)
		numelement = len(rcv)		
		msg = Int8()
		if numelement == 5:
			msg.data = int(rcv[3])
		else:
			msg.data = 9 	#error
		pub.publish(msg)
		rate.sleep()