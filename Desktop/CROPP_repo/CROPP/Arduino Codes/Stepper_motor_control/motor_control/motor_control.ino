
// Include the AccelStepper library:
#include <AccelStepper.h>

// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define dirPin1 5
#define stepPin1 6

#define dirPin2 1
#define stepPin2 2

#define whitePin 7
#define uvcPin 8

#define motorInterfaceType 1

// Create a new instance of the AccelStepper class:
AccelStepper stepper1 = AccelStepper(motorInterfaceType, stepPin1, dirPin1);
AccelStepper stepper2 = AccelStepper(motorInterfaceType, stepPin2, dirPin2);

void setup() {
	
	//Initializes serial communication
	Serial.begin(9600);
	
	// Set the maximum speed in steps per second:
	stepper1.setMaxSpeed(1000);
	stepper2.setMaxSpeed(1000);

	// Set the speed in steps per second:
	stepper1.setSpeed(800);
	stepper2.setSpeed(500);

	pinMode(whitePin,OUTPUT);
	pinMode(uvcPin,OUTPUT);
  
  
}

bool stepper1Status = false;
bool stepper2Status = false;
bool uvcStatus = false;
bool whiteStatus = false; 

void runMotors(){
	if(stepper1Status == true){
		 stepper1.runSpeed();  
	}
	if(stepper2Status == true){
	     stepper2.runSpeed();
	}
}



void loop() {
	
	if (Serial.available()) {  // check for incoming serial data
    String command = Serial.readStringUntil('\n');  // read command from serial port

   
    if(command == "stepper1On")
    {
      stepper1Status = true;
     
    } else if(command == "stepper1Off")
    {
      stepper1Status = false;
	  
    } else if(command == "stepper2On")
    {
      stepper2Status = true;
	  
    } else if(command == "stepper2Off")
    {
      stepper2Status = false;
	  
    } else if(command == "allStepperOff")
    {
      stepper1Status = false;
	  stepper2Status = false;
	  
    } else if(command == "toggleWhite")
    {
      whiteStatus = !whiteStatus;
	  digitalWrite(whitePin,whiteStatus);
	  
    } else if(command == "toggleUVC")
    {
      uvcStatus = !uvcStatus;
	  digitalWrite(uvcPin,uvcStatus);
	  
    } 
	
   
  } 
	runMotors();
	
	
}
