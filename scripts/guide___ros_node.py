#!/usr/bin/env python
import rospy
from sorabot.msg import linefollower_msg
from sorabot.msg import drivers_msg
from sorabot.msg import ultrasonic_msg
from sorabot.msg import kemet_msg
from sorabot.msg import colors_msg
from std_msgs.msg import Int8
from sorabot.msg import uvcontrol_msg

# Mario Soranno

followerSX = 9
followerSXC = 9
followerDXC = 9
followerDX = 9

ultrasonicF = 9
ultrasonicB = 9

kemetF = 9
kemetB = 9

SX_Red = 9
SX_Green = 9
SX_Blue = 9
DX_Red = 9
DX_Green = 9
DX_Blue = 9

uvcvalue = 9

SXRcount = 0
SXGcount = 0
SXBcount = 0
DXRcount = 0
DXGcount = 0
DXBcount = 0

def callback_linefollower(msglinef):
	global followerSX
	global followerSXC
	global followerDXC
	global followerDX
	followerSX = msglinef.followerSX
	followerSXC = msglinef.followerSXC
	followerDXC = msglinef.followerDXC
	followerDX = msglinef.followerDX

def callback_ultrasonic(msgultra):	
	global ultrasonicF
	global ultrasonicB
	
	ultrasonicF = msgultra.ultrasonicF
	ultrasonicB = msgultra.ultrasonicB

def callback_kemet(msgkemet):	
	global ultrasonicF
	global ultrasonicB
	
	kemetF = msgkemet.kemetF
	kemetB = msgkemet.kemetB

def callback_colors(msgcolors):
	global SX_Red
	global SX_Green
	global SX_Blue
	global DX_Red
	global DX_Green
	global DX_Blue

	global SXRcount
	global SXGcount
	global SXBcount
	global DXRcount
	global DXGcount
	global DXBcount
	
	if msgcolors.SX_Red == 1 and SXRcount < 2:
		SXRcount = SXRcount + 1
	elif msgcolors.SX_Red == 1 and SXRcount == 2:
		SX_Red = 1
	else:
		SX_Red = 0
		SXRcount = 0
	
	if msgcolors.SX_Green == 1 and SXGcount < 2:
		SXGcount = SXGcount + 1
	elif msgcolors.SX_Green == 1 and SXGcount == 2:
		SX_Green = 1
	else:
		SX_Green = 0
		SXGcount = 0
	
	if msgcolors.SX_Blue == 1 and SXBcount < 2:
		SXBcount = SXBcount + 1
	elif msgcolors.SX_Blue == 1 and SXBcount == 2:
		SX_Blue = 1
	else:
		SX_Blue = 0
		SXBcount = 0

	if msgcolors.DX_Red == 1 and DXRcount < 2:
		DXRcount = DXRcount + 1
	elif msgcolors.DX_Red == 1 and DXRcount == 2:
		DX_Red = 1
	else:
		DX_Red = 0
		DXRcount = 0
		
	if msgcolors.DX_Green == 1 and DXGcount < 2:
		DXGcount = DXGcount + 1
	elif msgcolors.DX_Green == 1 and DXGcount == 2:
		DX_Green = 1
	else:
		DX_Green = 0
		DXGcount = 0
		
	if msgcolors.DX_Blue == 1 and DXBcount < 2:
		DXBcount = DXBcount + 1
	elif msgcolors.DX_Blue == 1 and DXBcount == 2:
		DX_Blue = 1
	else:
		DX_Blue = 0
		DXBcount = 0
		

def callback_uvcvalue(msguvc):
	global uvcvalue
	
	uvcvalue = msguvc.data


if __name__ == '__main__':
	rospy.init_node('guide')
	pub_drivers = rospy.Publisher("drivers", drivers_msg, queue_size = 10)
	pub_uvcontrol = rospy.Publisher("uvcontrol", uvcontrol_msg, queue_size = 10)
	sub_linefollower = rospy.Subscriber("linefollower", linefollower_msg, callback_linefollower)	
	sub_ultrasonic = rospy.Subscriber("ultrasonic", ultrasonic_msg, callback_ultrasonic)	
	sub_kemet = rospy.Subscriber("kemet", kemet_msg, callback_kemet)	
	sub_colors = rospy.Subscriber("colors", colors_msg, callback_colors)
	sub_uvcvalue = rospy.Subscriber("uvcvalue", Int8, callback_uvcvalue)
	msgdri = drivers_msg()
	msguvc = uvcontrol_msg()	
	rate = rospy.Rate(10)
	inc = 0
	incuvc = 0
	stop = 0
	SX_Red_last = 0
	SX_Green_last = 0
	SX_Blue_last = 0
	DX_Red_last = 0
	DX_Green_last = 0
	DX_Blue_last = 0
	h_move = 0
	while not rospy.is_shutdown():
		incuvc = incuvc + 1
		msguvc.inc = incuvc
		inc = inc + 1
		msgdri.inc = inc
		msgdri.direction = 0
		
		if uvcvalue_test == 1:	# -------- UV-C present --------
			if ultrasonicF == 1 or ultrasonicB == 1 or kemetF == 1 or kemetB == 1:	# -------- pause --------
				msgdri.rotation = 0
				msgdri.velocity = 0
				msguvc.on = 0 			# UV-C Lamps off - vertical
				msguvc.horizontal = 0 	# vertical
			else:	# Line follower
				msgdri.velocity = 20
				if followerDXC == 0:		# -------- turn left --------
					msgdri.rotation = 1
					if h_move == 0:
						msguvc.on = 1 			# UV-C Lamps on - vertical
						msguvc.horizontal = 0 	# UV-C Lamps on - vertical
					stop = 0
				elif followerSXC == 0:		# -------- turn right --------
					msgdri.rotation = 3
					if h_move == 0:
						msguvc.on = 1 			# UV-C Lamps on - vertical
						msguvc.horizontal = 0 	# UV-C Lamps on - vertical
					stop = 0
				elif followerSX == 1 and followerSXC == 1 and followerDXC == 1 and followerDX == 1:	# -------- stop --------
					msgdri.rotation = 0
					msgdri.velocity = 0
					msguvc.on = 0 			# UV-C Lamps off - vertical
					msguvc.horizontal = 0 	# vertical
					stop = 1
				else:
					msgdri.rotation = 2	# go straight ahead
					if h_move == 0:
						msguvc.on = 1 			# UV-C Lamps on - vertical
						msguvc.horizontal = 0 	# UV-C Lamps on - vertical
					stop = 0

				# Colors SX				
				if stop == 0 and SX_Red == 1 and SX_Red_last != 1:		# UVGI point - vertical
					SX_Red_last = 1
					msgdri.rotation = 0
					msgdri.velocity = 0
					pub_drivers.publish(msgdri)
					msguvc.on = 1 						# UV-C Lamps off - vertical
					msguvc.horizontal = 0 				# vertical
					pub_uvcontrol.publish(msguvc)
					rospy.sleep(12)						# 12 seconds
				elif SX_Red == 0 and SX_Red_last == 1:
					SX_Red_last = 0
				elif stop == 0 and SX_Blue == 1:		# UVGI point - horizontal
					SX_Blue_last = 1
					msgdri.rotation = 0
					msgdri.velocity = 0
					pub_drivers.publish(msgdri)
					msguvc.on = 1 						# UV-C Lamps on - vertical
					msguvc.horizontal = 1 				# horizontal
					pub_uvcontrol.publish(msguvc)
					rospy.sleep(12)						# 12 seconds
				elif SX_Blue == 0 and SX_Blue_last == 1:
					SX_Blue_last = 0	
				elif stop == 0 and SX_Green == 1 and h_move == 0 and DX_Green_last == 0:	# UVGI point - horizontal in movement
					DX_Green_last = 1
					h_move = 1
					msguvc.on = 1 			# UV-C Lamps on - vertical
					msguvc.horizontal = 1 	# UV-C Lamps on - vertical
					pub_uvcontrol.publish(msguvc)
				elif SX_Green == 0 and DX_Green_last == 1:
					DX_Green_last = 0
				elif stop == 0 and SX_Green == 1 and h_move == 1 and DX_Green_last == 0:
					DX_Green_last = 1
					h_move = 0
				
		else:	# -------- UV-C not present --------
			msgdri.rotation = 0
			msgdri.velocity = 0
			msguvc.on = 0 				# UV-C Lamps off - vertical
			msguvc.horizontal = 0 		# UV-C Lamps on - vertical
	
		pub_uvcontrol.publish(msguvc)	
		pub_drivers.publish(msgdri)	
		rate.sleep()