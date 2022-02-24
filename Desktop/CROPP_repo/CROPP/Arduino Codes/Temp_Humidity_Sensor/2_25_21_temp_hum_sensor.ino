#include <dht.h>

dht DHT;

#define DHT11_PIN A2

void setup(){
  Serial.begin(9600);
}

void loop(){
  int chk = DHT.read11(DHT11_PIN);
  delay(1000); //delay added to avoid 999 reading
  Serial.print("Temperature (C) = ");
  Serial.println(DHT.temperature);
  Serial.print("Humidity (%) = ");
  Serial.println(DHT.humidity);
  delay(1000);
}
