#include <dht.h>

dht DHT;

//  Temp/Humidity Sensor Pin
#define DHT11_PIN 12

//  Linear Actuator Pins
#define act1Forward 12
#define act1Backward 13
#define act2Forward A0
#define act2Backward 15 // A1



unsigned long actStartTime[2];
bool act1State = LOW;
bool act2State = LOW;


const int pumpPins[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
bool pumpStatus[] = {LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW};


void setup() {

  
	Serial.begin(9600);
	for (int ii = 0; ii < (sizeof(pumpPins) / sizeof(pumpPins[0])); ii++) {
		pinMode(pumpPins[ii], OUTPUT);
	}
}

bool current = LOW;

void togglePumps(int index) {
  pumpStatus[index] = !pumpStatus[index];
  digitalWrite(pumpPins[index], pumpStatus[index]);
}



void toggleAct1(){
  actStartTime[0] = millis();
  digitalWrite(act1Forward,act1State);
  digitalWrite(act1Backward,!act1State);
}
void brakeAct1(){
  digitalWrite(act1Forward,HIGH);
  digitalWrite(act1Backward,HIGH);
  actStartTime[0] = 0;
}

void toggleAct2(){
  actStartTime[1] = millis();
  digitalWrite(act2Forward,act1State);
  digitalWrite(act2Backward,!act1State);
}
void brakeAct2(){
  digitalWrite(act2Forward,HIGH);
  digitalWrite(act2Backward,HIGH);
  actStartTime[1] = 0;
}

void loop() {
  
  if (Serial.available()) {  // check for incoming serial data
    String command = Serial.readStringUntil('\n');  // read command from serial port
    
	digitalWrite(13,HIGH);//DEBUGGING
	
    //      $pump01
    if (command.charAt(0) == '$') { //Indicates pump
      int index = command.substring(5).toInt();
      index -= 1;
      togglePumps(index);
      

    } else if(command == "getTH")
    {
      int chk = DHT.read11(DHT11_PIN);  
      Serial.println("" + String(DHT.humidity) + "!" + String(DHT.temperature) + "!");   
      
    } else if(command =="act1")
    { toggleAct1();
    } else if(command=="act2")
    { toggleAct1(); 
    }
    

  } 
if(actStartTime[0] - millis() > 2000){//If 2 seconds have passed since actuator started moving
   brakeAct1();
}
if(actStartTime[1] - millis() > 2000){//If 2 seconds have passed since actuator started moving
   brakeAct2();
}


}
