

//Number of pumps with pins from NUM_PUMPS-1 to NUM_PUMPS (Not inclusive)
  //If NUM_PUMPS == 2:   pumps on pins 0 & 1
#define NUM_PUMPS 1 

void setup() {

  for(int ii =0; ii<NUM_PUMPS;ii++){
    pinMode(ii,OUTPUT);
  }
  

}

void loop() {

  for(int jj=0; jj<NUM_PUMPS;jj++){
    digitalWrite(jj,HIGH);
  }

/* //Uncomment if you want pumps to alternate between on and off
  delay(1000); //Delay in microseconds
  for(int jj=0; jj<NUM_PUMPS;jj++){
    digitalWrite(jj,LOW);
  }
  delay(1000);
*/
  

}
