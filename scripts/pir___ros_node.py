#!/usr/bin/env python
import rospy
import serial
from betabot.msg import kemet_msg

# Jose Carlos Rangel

port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)

def readlineCR(port):
    rv = ""
    while True:
		ch = port.read()
		if ch != '\n':
			rv += ch
			if ch=='\r' or ch=='':
				return rv

if __name__ == '__main__':
	rospy.init_node('pir')
	pub = rospy.Publisher("/kemet_msg", kemet_msg, queue_size = 10)
	rate = rospy.Rate(10)
	inc = 0
	kemetF = 0
	kemetB = 0
	
	#print "evaluando"
	while not rospy.is_shutdown():	
		rcv = readlineCR(port)
		#print rcv
		arrayric = rcv.split(";")
		numelement = len(arrayric)
		if numelement == 4:
			arrayric[3] = arrayric[3].replace('\r', '')
			if arrayric[0] == "SF" and arrayric[2] == "SB":
				kemetF = int(arrayric[1])
				kemetB = int(arrayric[3])
				inc = inc + 1
				
		msg = kemet_msg()
		msg.inc = inc
		msg.kemetF = kemetF
		msg.kemetB = kemetB 
		
		pub.publish(msg)
		rate.sleep()