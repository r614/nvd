#include "HX711.h"

#define calibration_factor -7050.0 // This value is obtained using the SparkFun_HX711_Calibration sketch

#define DOUT 3
#define CLK 2

#define PWM 5
#define INA 7
#define INB 8

#define EN A0

// Movement Key
#define BACKWARD 1
#define FORWARD -1
#define TRIGGER_MOVE 1
#define CANCEL_MOVE -9

// Sync Status Key
#define ARDUINO_DISABLED -1
#define ARDUINO_READY 0
#define ARDUINO_ARMED 1
#define ARDUINO_MOVING 2
#define REQUEST_ARDUINO_STATUS 5

HX711 scale;
int status;
int x;
int signal;

void moveMotor(int mode)
{
  digitalWrite(EN, HIGH);

  if (mode == BACKWARD)
  {
    digitalWrite(INA, HIGH); // Backward
    digitalWrite(INB, LOW);
  }
  else
  {
    digitalWrite(INA, LOW); // Forward
    digitalWrite(INB, HIGH);
  }

  analogWrite(PWM, 255); // Speed control of Motor

  delay(15000);
  analogWrite(PWM, 0);
  digitalWrite(EN, LOW);
}

void moveMotorBackFive()
{
  digitalWrite(EN, HIGH);
  digitalWrite(INA, HIGH); // Backward
  digitalWrite(INB, LOW);

  analogWrite(PWM, 255); // Speed control of Motor
  delay(5000);
  analogWrite(PWM, 0);
  digitalWrite(EN, LOW);
}

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(1);
  scale.begin(DOUT, CLK);
  scale.set_scale(calibration_factor);
  scale.tare(); // Assuming there is no weight on the scale at start up, reset the scale to 0
  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(PWM, OUTPUT);
  pinMode(INA, OUTPUT);
  pinMode(INB, OUTPUT);
  pinMode(EN, OUTPUT);

  digitalWrite(LED_BUILTIN, LOW);
  moveMotorBackFive();

  status = ARDUINO_READY;
  Serial.println(status);
}

void sync()
{
  while (true)
  {
    while (!Serial.available()); // wait for input

    signal = Serial.readString().toInt();

    switch (signal)
    {
    case REQUEST_ARDUINO_STATUS:
      Serial.println(status);
      break;

    case TRIGGER_MOVE:
      status = ARDUINO_MOVING;
      Serial.println(status);
      moveMotor(FORWARD);
      moveMotor(BACKWARD);
      status = ARDUINO_READY;
      Serial.println(status);
      return;

    case CANCEL_MOVE:
      status = ARDUINO_READY;
      Serial.println(status);
      return;
    }
  }
}

void loop()
{
  if (scale.get_units() > 0.333)
  {
    // Weight Sensor is Armed
    digitalWrite(LED_BUILTIN, HIGH);
    sync();
    digitalWrite(LED_BUILTIN, LOW);
  }

  if (Serial.available() > 0) {
    signal = Serial.readString().toInt();

    if (signal == REQUEST_ARDUINO_STATUS) { 
      Serial.println(status);
    }
  }
}

void old_loop()
{
  if (scale.get_units() > 0.333)
  {
    digitalWrite(LED_BUILTIN, HIGH);
    while (!Serial.available()); // wait for input
    x = Serial.readString().toInt();
    if (x == TRIGGER_MOVE)
    {
      Serial.print(x + 1);

      // move forward and then back
      moveMotor(FORWARD);
      moveMotor(BACKWARD);
    }
    else if (x == CANCEL_MOVE)
    {
      Serial.println("Cancelling move");
    }
    else
    {
      Serial.println("Error; Command not found");
    }
    digitalWrite(LED_BUILTIN, LOW);
  }
}
