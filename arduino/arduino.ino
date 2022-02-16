int x;

#include "HX711.h"

#define calibration_factor -7050.0 //This value is obtained using the SparkFun_HX711_Calibration sketch

#define DOUT  3
#define CLK  2

#define PWM 5
#define INA 7
#define INB 8

#define EN A0

#define BACKWARD 1
#define FORWARD -1 
#define TRIGGER_MOVE 1 
#define CANCEL_MOVE -1


HX711 scale;

void moveMotor(int mode) {
  digitalWrite(EN,HIGH);

  if (mode == BACKWARD) { 
    digitalWrite(INA,HIGH); //Backward
    digitalWrite(INB,LOW);
  } else { 
    digitalWrite(INA,LOW); //Forward
    digitalWrite(INB,HIGH);
  }
 
  analogWrite(PWM,255); //Speed control of Motor

  delay(15000);
  analogWrite(PWM, 0); 
  digitalWrite(EN,LOW);  
}

void moveMotorBackFive() { 
  digitalWrite(EN,HIGH);
  digitalWrite(INA,HIGH); //Backward
  digitalWrite(INB,LOW);

  analogWrite(PWM,255); //Speed control of Motor
  delay(5000);
  analogWrite(PWM, 0); 
  digitalWrite(EN,LOW);  
}

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  scale.begin(DOUT, CLK);
  scale.set_scale(calibration_factor);
  scale.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0
  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(PWM,OUTPUT);
  pinMode(INA,OUTPUT);
  pinMode(INB,OUTPUT);
  pinMode(EN,OUTPUT);
  
  digitalWrite(LED_BUILTIN, LOW); 
  moveMotorBackFive();
}



void loop() {
 if (scale.get_units() > 0.333) { 
   digitalWrite(LED_BUILTIN, HIGH);  
   while (!Serial.available()); // wait for input
   x = Serial.readString().toInt();
   if (x == TRIGGER_MOVE) { 
    Serial.print(x + 1);
    
    // move forward and then back
    moveMotor(FORWARD); 
    moveMotor(BACKWARD);
   } else if (x == CANCEL_MOVE) {
    Serial.println("Cancelling move");
   }
   else { 
    Serial.println("Error; Command not found"); 
   }
   digitalWrite(LED_BUILTIN, LOW);    
 }
}
