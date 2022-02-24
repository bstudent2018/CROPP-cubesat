/*
 */
 

int pins = 4;
int led[] = {10,11,12,13};
unsigned long int wait = 15000; // 86396900;
unsigned int run = 3100;
int iteration = 0;

// the setup routine runs once when you press reset:  
void setup() {
  for (int i = 0; i < 4; i++) {
  pinMode(led[i], OUTPUT);
  Serial.begin(9600);
  }  
}

// the loop routine runs over and over again forever:
void loop() {
  unsigned int day_elapsed = millis() / 1000 / 60 / 60 / 24;
  unsigned int hour_elapsed = millis() / 1000 / 60 / 60 - (day_elapsed * 24);
  unsigned int min_elapsed = millis() / 1000 / 60 - (day_elapsed * 24 * 60) - (hour_elapsed * 60);
  unsigned int sec_elapsed = millis() / 1000 - (day_elapsed * 24 * 60 * 60) - (hour_elapsed * 60 * 60) - (min_elapsed * 60);
  Serial.print("watering run #: ");
  Serial.print(iteration);
  Serial.print(" at elapsed time ");
  Serial.print(day_elapsed);
  Serial.print("d ");
  Serial.print(hour_elapsed);
  Serial.print(":");
  Serial.print(min_elapsed);
  Serial.print(":");
  Serial.print(sec_elapsed);
  Serial.print("\n");
  
  for(int i = 0; i < pins; i++)
  {
  digitalWrite(led[i], LOW);
  //delay(0);
  } 
  delay(run);               // wait for a second
  for(int i = 0; i < pins; i++)
  {
  digitalWrite(led[i], HIGH);
  //delay(0)
  }  
  delay(wait);
  // wait for a second
  iteration++;
  
  //Briana-written Code
  //adding different run tim
  for(int i = 0; i < pins; i++)
  {
  digitalWrite(led[i], LOW);
  //delay(0);
  } 
  delay(run);               // wait for a second
  for(int i = 0; i < pins; i++)
  {
  digitalWrite(led[i], HIGH);
  //delay(0)
  }  
  delay(wait);
  // wait for a second
  iteration++;
}
