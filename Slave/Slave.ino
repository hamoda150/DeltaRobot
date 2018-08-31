#include <Servo.h>
#include<math.h>

// global variables
String incoming;
int pulse = 0;
int arr[4]; // array to hold pulses
int i = 0;     // counter for arr
int CounterSensor_state = 0;
int last_CounterSensor_state = 1;
int StopSensor_state = 0;
int last_StopSensor_state = 1;
int Product_counter = 0;
int MotorWorkingFlag = 0;
Servo myservo1;  // create servo object to control a servo
Servo myservo2;
Servo myservo3;
const int MotorBelt1 = 2;
const int MotorBelt2 = 3;
//const int CounterSensor = 4;
//const int StopSensor = 5;
const int Buzzer = 6;
// this constant won't change:
const int  buttonPin = 4;    // the pin that the pushbutton is attached to


// Variables will change:
int buttonPushCounter = 0;   // counter for the number of button presses
int buttonState = 0;         // current state of the button
int lastButtonState = 0;     // previous state of the button
// function prototypes
void arr_handling(int pulse);
int Motor_map(int pulse);

void setup() {
        Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
        myservo1.attach(9);  // attaches the servo on pin 9 to the servo object
        myservo2.attach(10);
        myservo3.attach(11);
        pinMode(MotorBelt1, OUTPUT);
        pinMode(MotorBelt2, OUTPUT);
       // pinMode(CounterSensor, INPUT);
       // pinMode(StopSensor, INPUT);
        pinMode(Buzzer, OUTPUT);
        // initialize the button pin as a input:
        pinMode(buttonPin, INPUT);

}

void loop() 
{
   //##########################################//
  //    Start motor if there is any command   //
  //##########################################//
  if(MotorWorkingFlag == 0) // Motor ON
  {
    digitalWrite(MotorBelt1, HIGH);
    digitalWrite(MotorBelt2, LOW);  
  }
  if(MotorWorkingFlag == 1) // Motor OFF
  {
    digitalWrite(MotorBelt1, LOW);
    digitalWrite(MotorBelt2, LOW);      
  }
   //##############################################//
  //      Receive pulses from Raspberry pi        //
  //##############################################//
  if (Serial.available() > 0) 
  {
    // read the incoming byte:
    incoming=Serial.readStringUntil('\n');
    pulse = incoming.toInt();
    arr_handling(pulse);
    Serial.println("I Received:");
  //  Serial.println(arr[0]);
  //  Serial.println(arr[1]);
  //   Serial.println(arr[2]);
  }
// 45 deg
//  myservo1.write(Motor_map(1268));              // tell servo to go to position in variable 'pos'
 // myservo2.write(Motor_map(1268));
 // myservo3.write(Motor_map(1268));
/*
  //##############################################//
  //    counter sensor  (1 push counts 1 count) //
  //##############################################//
  // High state activation // when laser is on, LDR resistance becomes zero and high voltage is read
  CounterSensor_state = digitalRead(CounterSensor);
  StopSensor_state = digitalRead(StopSensor);

  if(CounterSensor_state == LOW) // use while(){} to wait until the state changes
    {
      Product_counter++;
      digitalWrite(Buzzer, HIGH);
      //LCD_Printf("%4d",Product_counter);
      Serial.println(Product_counter);
      while(CounterSensor_state == LOW)
      {
        CounterSensor_state = digitalRead(CounterSensor);
      //  Serial.println("I'm stucked at low state!");
      } // do nothing until product is removed
    }
  
  //##########################################//
  //      Stop sensor (interrupt)     //
  //##########################################//
  // High state activation
  if(StopSensor_state == LOW)
    {
      // Stop the conv belt
      digitalWrite(MotorBelt1, LOW);
      digitalWrite(MotorBelt2, LOW);
      Serial.println("Motor stopped due to sensor!");
      while(StopSensor_state == LOW){StopSensor_state = digitalRead(StopSensor);} // wait until the state changes
    }

 */ 
//////////////////////////////////////////////
/*
   // read the pushbutton input pin:
  buttonState = digitalRead(buttonPin);
  // compare the buttonState to its previous state
  if (buttonState != lastButtonState) {
    // if the state has changed, increment the counter
    if (buttonState == HIGH) {
      // if the current state is HIGH then the button went from off to on:
      buttonPushCounter++;
      Serial.println("on");
      Serial.print("number of button pushes: ");
      Serial.println(buttonPushCounter);
    } else {
      // if the current state is LOW then the button went from on to off:
      Serial.println("off");
    }
    // Delay a little bit to avoid bouncing
    delay(50);
  }
  // save the current state as the last state, for next time through the loop
  lastButtonState = buttonState;


  // turns on the LED every four button pushes by checking the modulo of the
  // button push counter. the modulo function gives you the remainder of the
  // division of two numbers:
  if (buttonPushCounter % 4 == 0) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }

  */
}

int Motor_map(int pulse)
{
  // Linear equation to map beween angles and pulses
 // int ServoAngle = (0.10909 * pulse) - 70.90909;
  int ServoAngle = map(pulse, 650, 2300, 0, 180);
  return ServoAngle;
}

void arr_handling(int pulse)
{
  arr[i] = pulse;
  MotorWorkingFlag = arr[0];
  if(i == 3)
  {
      // move servo motors
      Serial.println(arr[0]);
      Serial.println(arr[1]);
      Serial.println(arr[2]);
      Serial.println(arr[3]);
      
      myservo1.write(Motor_map(arr[1]));              // tell servo to go to position in variable 'pos'
      myservo2.write(Motor_map(arr[2]));
      myservo3.write(Motor_map(arr[3]));
  }
  i++;
  if(i > 3)  i=0;
}



