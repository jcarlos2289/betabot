#!/usr/bin/env python
import rospy
import serial
from sorabot.msg import colors_msg

# Mario Soranno

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
	rospy.init_node('colors')
	pub = rospy.Publisher("/colors_msg", colors_msg, queue_size = 10)
	rate = rospy.Rate(10)
	inc = 0
	sxR = 0
	sxG = 0
	sxB = 0
	dxR = 0
	dxG = 0
	dxB = 0
	while not rospy.is_shutdown():	
		rcv = readlineCR(port)
		arrayric = rcv.split(";")
		numelement = len(arrayric)
		if numelement == 8:
			arrayric[7] = arrayric[7].replace('\r', '')
			if arrayric[0] == "SX" and arrayric[4] == "DX":
				sxR = int(arrayric[1])
				sxG = int(arrayric[2])
				sxB = int(arrayric[3])
				dxR = int(arrayric[5])
				dxG = int(arrayric[6])
				dxB = int(arrayric[7])
				inc = inc + 1
				
		msg = colors_msg()
		msg.inc = inc
		msg.SX_Red = 0
		msg.SX_Green = 0 
		msg.SX_Blue = 0
		msg.DX_Red = 0
		msg.DX_Green = 0 
		msg.DX_Blue = 0
		# SX
		if sxR < sxB and sxR < sxG and sxR < 20:
			if sxR <=10 and sxG <=10 and sxB <=10:
				msg.SX_Red = 0
				msg.SX_Green = 0 
				msg.SX_Blue = 0
			else:
				msg.SX_Red = 1
				msg.SX_Green = 0 
				msg.SX_Blue = 0
		elif sxB < sxR and sxB < sxG:
			if sxR <=10 and sxG <=10 and sxB <= 10:
				msg.SX_Red = 0
				msg.SX_Green = 0 
				msg.SX_Blue = 0
			else:
				msg.SX_Red = 0
				msg.SX_Green = 0 
				msg.SX_Blue = 1
		elif sxG < sxR and sxG < sxB:
			if sxR <= 10 and sxG <=10 and sxB <= 10:
				msg.SX_Red = 0
				msg.SX_Green = 0 
				msg.SX_Blue = 0				
			else:
				msg.SX_Red = 0
				msg.SX_Green = 1
				msg.SX_Blue = 0
		else:
			msg.SX_Red = 0
			msg.SX_Green = 0 
			msg.SX_Blue = 0
		
		# DX
		if dxR < dxB and dxR < dxG and dxR < 20:
			if dxR <=10 and dxG <=10 and dxB <=10:
				msg.DX_Red = 0
				msg.DX_Green = 0 
				msg.DX_Blue = 0
			else:
				msg.DX_Red = 1
				msg.DX_Green = 0 
				msg.DX_Blue = 0
		elif dxB < dxR and dxB < dxG:
			if dxR <=10 and dxG <=10 and dxB <= 10:
				msg.DX_Red = 0
				msg.DX_Green = 0 
				msg.DX_Blue = 0
			else:
				msg.DX_Red = 0
				msg.DX_Green = 0 
				msg.DX_Blue = 1
		elif dxG < dxR and dxG < dxB:
			if dxR <= 10 and dxG <=10 and dxB <= 10:
				msg.DX_Red = 0
				msg.DX_Green = 0 
				msg.DX_Blue = 0			
			else:
				msg.DX_Red = 0
				msg.DX_Green = 1
				msg.DX_Blue = 0
		else:
			msg.DX_Red = 0
			msg.DX_Green = 0 
			msg.DX_Blue = 0

		pub.publish(msg)
		rate.sleep()