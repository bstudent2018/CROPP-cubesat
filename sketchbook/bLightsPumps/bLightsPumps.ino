//Pump variables
  const int numPins = 4; //amount of pins in use
  const int relayPin[] = {10,11,12,13}; //where the pins are connected to the Arduino board
  unsigned long int wait = 86400000; //[ms], wait for 1 day (86396900 ms)
  unsigned int run = 3500; //[ms], run for 3.1 seconds
  int runNum = 0; //set Run Number to 0
//Time-keeping variables
  const int ledPin = 9; //location of LED Pin
  int ledState = LOW;
  unsigned long previousms = 0; //[ms], last recorded time
  const long interval = 1000; //[ms], 1 second interval

//Setup Routine
void setup(){
  //Timekeeper Setup
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  
  //Pump Relay Loop
  for(int i = 0; i < numPins; i++) {
      pinMode(relayPin[i], OUTPUT);
  }
  for(int i = 0; i < numPins; i++) {
    digitalWrite(relayPin[i], LOW);
  }
  delay(600);  //fill the tubes with water for 0.6 seconds
  for (int i = 0; i < numPins; i++) {
    digitalWrite(relayPin[i], HIGH);
    }
  delay(5000);
}

void loop(){
  //setup for readable Time
  unsigned int dayNum = millis() / 1000 / 60 / 60 / 24;
  unsigned int hrNum = millis() / 1000 / 60 / 60 - (dayNum * 24);
  unsigned int minNum = millis() / 1000 / 60 - (dayNum * 24 * 60) - (hrNum * 60);
  unsigned int secNum = millis() / 1000 - (dayNum * 24 * 60 * 60) - (hrNum * 60 * 60) - (minNum * 60);
  
  //Pump Relay Loop
  for(int i = 0; i < numPins; i++) {
    digitalWrite(relayPin[i], LOW);
  } 
  delay(run); // wait for 3.1 seconds (watering run time)
  for(int i = 0; i < numPins; i++) {
    digitalWrite(relayPin[i], HIGH);
  }  
  delay(wait); // wait for 1 day (wait run time)
  /*
  //if the current time has exceeded the interval
  if (millis() - previousms >= interval){ 
    previousms = millis();
    
    //turn the LED on/off
    if (ledState == LOW){
      ledState = HIGH;
    } else {
      ledState = LOW;
    }
    digitalWrite(ledPin, ledState);
  }*/

  //display Time
  Serial.print("watering run #:\n");
  Serial.print(runNum);
  Serial.print(" at elapsed time ");
  Serial.print(dayNum);
  Serial.print("d ");
  Serial.print(hrNum);
  Serial.print(":");
  Serial.print(minNum);
  Serial.print(":");
  Serial.print(secNum);
  Serial.print("\n");

  runNum++; //increase the Run Number
}
