//Code adapted from Source: https://lastminuteengineers.com/a4988-stepper-motor-driver-arduino-tutorial/
// Define pin connections & motor's steps per revolution
const int dirPin1 = 5;
const int stepPin1 = 6;

const int dirPin2 = 1;
const int stepPin2 =2;

const int stepsPerRevolution = 200;

void setup()
{
  // Declare pins as Outputs
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
}
void loop()
{
  // Set motor direction clockwise
  digitalWrite(dirPin1, HIGH);
    digitalWrite(dirPin2, HIGH);
/*
  // Spin motor slowly
  for(int x = 0; x < stepsPerRevolution; x++)
  {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(2000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(2000);
  }
  delay(1000); // Wait a second
}*/
  /*// Set motor direction counterclockwise
  digitalWrite(dirPin, LOW);*/

  // Spin motor quickly
  for(int x = 0; x < stepsPerRevolution; x++)
  {
    digitalWrite(stepPin1, HIGH);
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin1, LOW);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(1000);
  }
  //delay(1000); // Wait a second
}
