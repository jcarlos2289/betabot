// Mario Soranno
#include <Servo.h>

// UVC Sensor
int sensorPin = A1;
int sensorValue = 0;

// HC-SR04
const int trigPin = 7;
const int echoPin = 6;
int distance; // variable for the distance measurement

// SERVO
Servo myservo;  // create servo object to control a servo
int pos = 0;    // variable to store the servo position

// SSR
const int ssr = 13;

void setup() {
  Serial.begin(9600);
  // SERVO
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(10);
  // HC-SR04
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  // SSR
  pinMode(ssr, OUTPUT);
  digitalWrite(ssr, LOW);
}

void loop() {
  sensorValue = analogRead(sensorPin);    // read the value from the UV sensor
  if (sensorValue > 40) Serial.println("UVC1");
  else Serial.println("UVC0");
  

  if (Serial.available()) {
     byte command = Serial.read();
     switch (command) 
      {
      case '0': // Vertical - UVC ON
        for (pos = myservo.read(); pos >= 10; pos -= 1) {
          myservo.write(pos);             
          delay(15);                       
        }
        digitalWrite(ssr, HIGH);
      break;
      case '1': // Horizontal - UVC ON
        for (pos = myservo.read(); pos <= 100; pos += 1) {
            myservo.write(pos);              
            distance = ultrasonic();
            if(distance<20) distance = ultrasonic();
            if(distance<20) break;
            delay(15);
          }
          digitalWrite(ssr, HIGH);
      break;
      case '2': // Vertical - UVC OFF
        for (pos = myservo.read(); pos >= 10; pos -= 1) {
          myservo.write(pos);              
          delay(15);                            
        }
        digitalWrite(ssr, LOW);
      break;
     }
     while (Serial.available()) {
       byte a = Serial.read();
     }
   }
  delay(100);
}

int ultrasonic(void)
{
  int dist;
  long duration;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(20);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  dist = (duration*0.034)/2;
  return dist;
}