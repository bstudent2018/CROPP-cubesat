
// Include the AccelStepper library:
//#include <AccelStepper.h>

// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define dirPin1 1
#define stepPin1 2

#define dirPin2 5
#define stepPin2 6

#define whitePin 7
#define uvcPin 8

//Stepper steps per 1/4 revolution (90 degrees)
const int stepsPerQuarterRevolution = 5000;
//Stepper steps per 1 revolution (360 degrees)
const int stepsPerRevolution = stepsPerQuarterRevolution * 4;
//Stepper steps per total movement of growth belt to next position
const int stepsPerMovement = stepsPerRevolution * 4;



//#define motorInterfaceType 1

// Create a new instance of the AccelStepper class:
//AccelStepper stepper1 = AccelStepper(motorInterfaceType, stepPin1, dirPin1);
//AccelStepper stepper2 = AccelStepper(motorInterfaceType, stepPin2, dirPin2);

void setup() {
	
	//Initializes serial communication
	Serial.begin(9600);
	
	// Set the maximum speed in steps per second:
//	stepper1.setMaxSpeed(1000);
//	stepper2.setMaxSpeed(1000);

	// Set the speed in steps per second:
//	stepper1.setSpeed(800);
//	stepper2.setSpeed(500);

  //Set Stepper Motor Pins
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);

	pinMode(whitePin,OUTPUT);
	pinMode(uvcPin,OUTPUT);
  
  
}

bool stepper1Status = false;
bool stepper2Status = false;
bool uvcStatus = false;
bool whiteStatus = false; 

//void runMotors(){
//	if(stepper1Status == true){
//		 stepper1.runSpeed();  
//	}
//	if(stepper2Status == true){
//	     stepper2.runSpeed();
//	}
//}
//


//Flags to tell if belt is at starting position(LOW) or ending position(HIGH)
bool stepper1Location = LOW;
bool stepper2Location = LOW;


void setMotorDirection(){
  digitalWrite(dirPin1, stepper1Location);
  digitalWrite(dirPin2, stepper2Location);
}

unsigned long currentSteps =0;
void runMotors(){
  setMotorDirection();
  digitalWrite(stepPin1, HIGH);
  digitalWrite(stepPin2, HIGH);
  delayMicroseconds(700);
  digitalWrite(stepPin1, LOW);
  digitalWrite(stepPin2, LOW);
  delayMicroseconds(700);
  currentSteps++;

  if(currentSteps >= stepsPerMovement){
    stepper1Status = false;
    stepper2Status = false;
    currentSteps = 0;
    stepper1Location = HIGH;
    stepper2Location = HIGH;
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
  if(stepper1Status ==true && stepper2Status==true){
	  runMotors();
  }
	
}
