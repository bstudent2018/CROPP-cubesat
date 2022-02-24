
#define line1Forward 12
#define line1Backward 13

#define line2Forward A0
#define line2Backward 15 // A1

void setup() {
    pinMode(line1Forward,OUTPUT);
    pinMode(line1Backward,OUTPUT);
    pinMode(line2Forward,OUTPUT);
    pinMode(line2Backward,OUTPUT);

}


void extend(int actNum){
    if(actNum == 1){
      digitalWrite(line1Forward,LOW);
      digitalWrite(line1Backward,HIGH);
    }
    if(actNum == 2){
      digitalWrite(line2Forward,LOW);
      digitalWrite(line2Backward,HIGH);
    }
  
  }

void brake(int actNum){
   if(actNum == 1){
      digitalWrite(line1Forward,HIGH);
      digitalWrite(line1Backward,HIGH);
    }
    if(actNum == 2){
      digitalWrite(line2Forward,HIGH);
      digitalWrite(line2Backward,HIGH);
    }
}

void retract(int actNum){
   if(actNum == 1){
      digitalWrite(line1Forward,HIGH);
      digitalWrite(line1Backward,LOW);
    }
    if(actNum == 2){
      digitalWrite(line2Forward,HIGH);
      digitalWrite(line2Backward,LOW);
    }
}

void loop() {

  extend(1);
  extend(2);
  delay(2000);
  brake(1);
  brake(2);
  delay(2000);
  retract(1);
  retract(2);
  delay(2000);
  




}
