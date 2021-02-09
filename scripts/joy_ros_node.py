#!/usr/bin/env python
import rospy
from betabot.msg import drivers_msg
from sensor_msgs.msg import Joy

# Jose Carlos Rangel



def callback_joy(joydata):
    msgdri = drivers_msg()
    #inc = inc + 1
    msgdri.inc = 12 #inc
    msgdri.direction = 0
    msgdri.rotation = 0
    msgdri.velocity = 15
	
    ejeDir = 4*joydata.axes[1]
    ejeRot = 4*joydata.axes[2]
    
    stopButton = joydata.buttons[0]
    
    if ejeDir > 0:
		msgdri.direction = 1
    elif ejeDir < 0:
		msgdri.direction = 0
    else: 
        msgdri.direction = 0
   
    if ejeRot > 0:
        msgdri.rotation = 1
    elif ejeRot < 0:
        msgdri.rotation = 3
    else: 
        msgdri.rotation = 2
    
    if stopButton == 1 :
		msgdri.direction = 0
		msgdri.rotation = 0
		msgdri.velocity = 0	
		pub.publish(msgdri)
    else:
		pub.publish(msgdri)	



def start():
	# publishing to "drivers topic" to control turtle1
    global pub
    pub = rospy.Publisher("drivers", drivers_msg, queue_size = 10)
    global inc
    inc = 0
    # subscribed to joystick inputs on topic "joy"
    rospy.Subscriber("joy", Joy, callback_joy)
    # starts the node
    rospy.init_node('joy_control')
    rospy.spin()
			

if __name__ == '__main__':
	inc = 0
	start()
