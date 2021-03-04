#include <dht.h>

dht DHT;

#define DHT11_PIN 12

const unsigned long probeInterval = 5000; //Time between checking temperature and humidity (In milliseconds)
float temp;
float humidity;
unsigned long startTime;

const int pumpPins[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,13};
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

  startTime = millis();

}



void loop() {
  
  if (Serial.available()) {  // check for incoming serial data
    String command = Serial.readString();  // read command from serial port
    digitalWrite(13,HIGH);
    //      $pump01
    if (command.charAt(0) == '$') { //Indicates pump
      int index = command.substring(5).toInt();
      index -= 1;
      togglePumps(index);
      

    } else if(command == "getTemp")
    {
      int chk = DHT.read11(DHT11_PIN);
      
      
      Serial.println("T: "+String(DHT.temperature)); 
     
    } else if(command == "getHumid")
    {
      int chk = DHT.read11(DHT11_PIN);
      
      Serial.println(String(DHT.humidity));
    }
    
    

  } 
else{
digitalWrite(13,LOW);
}

}
