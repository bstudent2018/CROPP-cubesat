//Code created by:http://www.learningaboutelectronics.com/Articles/Peristaltic-pump-circuit-with-an-arduino-microcontroller.php

//The code to turn on a peristaltic pump for 5 seconds every 30 seconds is shown below.

const int motor= 10; //LED connected to digital pin 10

void setup()
{
pinMode(motor, OUTPUT); //sets the digital pin as output
}

void loop()
{
digitalWrite(motor,HIGH); //turns the LED on
delay(5000);
digitalWrite(motor,LOW);
delay(30000);
}
