//Includes the Arduino Stepper Library
#include <Stepper.h>

// Defines the number of steps per rotation
const int stepsPerRevolution = 2048;

// Creates an instance of stepper class
// Pins entered in sequence IN1-IN3-IN2-IN4 for proper step sequence
Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);

void releaseMotor() {
  digitalWrite(8, LOW);
  digitalWrite(9, LOW);
  digitalWrite(10, LOW);
  digitalWrite(11, LOW);
}

void setup() {
  // Nothing to do (Stepper Library sets pins as outputs)
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {

    int inputAngle = Serial.parseInt();
    if (inputAngle >= 0 && inputAngle <= 360){
      myStepper.setSpeed(5);
      myStepper.step(stepsPerRevolution/60);
      Serial.print("Rotating to ");
      Serial.print(inputAngle);
      delay(1000);
      releaseMotor();
    }
    if (inputAngle <= 0 && inputAngle >= -360){
      myStepper.setSpeed(5);
      myStepper.step(-stepsPerRevolution/60);
      Serial.print("Rotating to ");
      Serial.print(inputAngle);
      delay(1000);
      releaseMotor();
    }
  }
}