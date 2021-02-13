// Mario Soranno
#include "wiringPi.h"
#include "ros/ros.h"
#include "betabot/ultrasonic_msg.h"

// Mario Soranno

int main(int argc, char **argv)
	{
	ros::init(argc, argv, "ultrasonic");	
	ros::NodeHandle node_obj;
	ros::Publisher pub = node_obj.advertise<betabot::ultrasonic_msg>("ultrasonic",10);
	betabot::ultrasonic_msg msg;
	ros::Rate loop_rate(10);
	wiringPiSetup();
	pinMode(6, OUTPUT);
	pinMode(10, INPUT);
	pinMode(11, OUTPUT);
	pinMode(12, INPUT);
	ros::Time begin = ros::Time::now();
	ros::Time stop = ros::Time::now();
	float distanceF = 0;
	float distanceB = 0;
	uint64_t difference = 0;
	uint64_t TrigDuration = 0;
	uint64_t inc = 0;
	while(ros::ok())
		{
		distanceF = 0;
		difference = 0;
		TrigDuration = 0;
		digitalWrite(6, HIGH);
		begin = ros::Time::now();
		while(TrigDuration < 12000)
			{
			stop = ros::Time::now();	
			TrigDuration = stop.toNSec() - begin.toNSec();	
			}
		digitalWrite(6, LOW);
		while(!digitalRead(10));
		begin = ros::Time::now();
		while(digitalRead(10));
		stop = ros::Time::now();
		difference = stop.toNSec() - begin.toNSec();
		distanceF = (difference * (340.0 / 1000000000.0)) / 2.0;
		
		distanceB = 0;
		difference = 0;
		TrigDuration = 0;
		digitalWrite(11, HIGH);
		begin = ros::Time::now();
		while(TrigDuration < 12000)
			{
			stop = ros::Time::now();	
			TrigDuration = stop.toNSec() - begin.toNSec();	
			}
		digitalWrite(11, LOW);
		while(!digitalRead(12));
		begin = ros::Time::now();
		while(digitalRead(12));
		stop = ros::Time::now();
		difference = stop.toNSec() - begin.toNSec();
		distanceB = (difference * (340.0 / 1000000000.0)) / 2.0;

		inc++;
		msg.inc = inc;
		if(distanceF < 0.30) msg.ultrasonicF = 1;
		else msg.ultrasonicF = 0;
			
		if(distanceB < 0.30) msg.ultrasonicB = 1;
		else msg.ultrasonicB = 0;
		
		pub.publish(msg);
		ros::spinOnce();
		loop_rate.sleep();
		}
	return 0;
	}
