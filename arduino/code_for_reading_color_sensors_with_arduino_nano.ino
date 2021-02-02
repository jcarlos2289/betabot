// Mario Soranno
const int s0 = 9;         // Output frequency scaling selection
const int s1 = 8;         // Output frequency scaling selection
const int s2 = 6;         // Photodiode type selection
const int s3 = 7;         // Photodiode type selection
const int outSX = 4;      // Output frequency - SX: left Sensor Module 
const int outDX = 5;      // Output frequency - SX: right Sensor Module 
const int led = 10;       // white LEDs control
int brightness = 255;     // brightness of LEDs

int redSX = 0;            // Red value - SX: left Sensor Module 
int greenSX = 0;          // Green value - SX: left Sensor Module 
int blueSX = 0;           // Blue value - SX: left Sensor Module 

int redDX = 0;            // Red value - DX: left Sensor Module 
int greenDX = 0;          // Green value - DX: left Sensor Module 
int blueDX = 0;           // Blue value - DX: left Sensor Module 

void setup()   
{  
  Serial.begin(9600); 
 
  pinMode(s0, OUTPUT);  
  pinMode(s1, OUTPUT);  
  pinMode(s2, OUTPUT);  
  pinMode(s3, OUTPUT);
  pinMode(led, OUTPUT);  
  pinMode(outSX, INPUT);   
  pinMode(outDX, INPUT); 
  
  digitalWrite(s0, HIGH);  
  digitalWrite(s1, HIGH);
  analogWrite(led, brightness);
} 
 
void loop() 
{  
  colors();
  Serial.print("SX;");  
  Serial.print(redSX, DEC);  
  Serial.print(";");  
  Serial.print(greenSX, DEC);  
  Serial.print(";");  
  Serial.print(blueSX, DEC);

  Serial.print(";DX;");  
  Serial.print(redDX, DEC);  
  Serial.print(";");  
  Serial.print(greenDX, DEC);  
  Serial.print(";");  
  Serial.println(blueDX, DEC);  

  delay(100);         // 100ms delay
}
void colors()
{
  digitalWrite(s2, LOW);    // Read value
  digitalWrite(s3, LOW);
  redSX = pulseIn(outSX, digitalRead(outSX) == HIGH ? LOW : HIGH);    // Reads a pulse (either HIGH or LOW) on a pin.
  redDX = pulseIn(outDX, digitalRead(outDX) == HIGH ? LOW : HIGH);    // Reads a pulse (either HIGH or LOW) on a pin.
  digitalWrite(s3, HIGH);   // Blue value
  blueSX = pulseIn(outSX, digitalRead(outSX) == HIGH ? LOW : HIGH);   // Reads a pulse (either HIGH or LOW) on a pin.
  blueDX = pulseIn(outDX, digitalRead(outDX) == HIGH ? LOW : HIGH);   // Reads a pulse (either HIGH or LOW) on a pin.
  digitalWrite(s2, HIGH);   // Green value
  greenSX = pulseIn(outSX, digitalRead(outSX) == HIGH ? LOW : HIGH);  // Reads a pulse (either HIGH or LOW) on a pin.
  greenDX = pulseIn(outDX, digitalRead(outDX) == HIGH ? LOW : HIGH);  // Reads a pulse (either HIGH or LOW) on a pin.
}