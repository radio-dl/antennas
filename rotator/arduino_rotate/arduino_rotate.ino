//Includes the Arduino Stepper Library
#include <Stepper.h>

// Defines the number of steps per rotation
const int stepsPerRevolution = 2048;
int divisor = 180; // 360 / 180 gives 2 degrees.
int current_position = 0;

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
  Serial.begin(115200);
  delay(1000);
  while (Serial.available()) Serial.read();
  myStepper.setSpeed(1);
  myStepper.step(0);
  delay(3000);
}

void loop() {
  if (Serial.available() > 0) {

    int inputAngle = Serial.parseInt();
    while (Serial.available()) Serial.read();
    
    divisor = 360 / inputAngle;
    if (inputAngle >= 0 && inputAngle <= 360){
      myStepper.setSpeed(1);
      myStepper.step(0);  // wakes the motor
      delay(100);         // give coils time to energize
      myStepper.setSpeed(1);
      myStepper.step(stepsPerRevolution/divisor);
      Serial.print("Rotating ");
      Serial.print(inputAngle);
      Serial.print("\n");
      current_position=current_position+inputAngle;
      Serial.print("Current position: ");
      Serial.print(current_position);
      Serial.print("\n");
      delay(1000);
      releaseMotor();
    }
    if (inputAngle <= 0 && inputAngle >= -360){
      myStepper.setSpeed(1);
      myStepper.step(0);  // wakes the motor
      delay(100);         // give coils time to energize
      myStepper.setSpeed(1);
      myStepper.step(stepsPerRevolution/divisor);
      Serial.print("Rotating ");
      Serial.print(inputAngle);
      Serial.print("\n");
      current_position=current_position+inputAngle;
      Serial.print("Current position: ");
      Serial.print(current_position);
      Serial.print("\n");
      delay(1000);
      releaseMotor();
    }
  }
}