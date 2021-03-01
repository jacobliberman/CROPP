#include <Adafruit_Si7021.h>

Adafruit_Si7021 THsensor = Adafruit_Si7021();

const unsigned long probeInterval = 5000; //Time between checking temperature and humidity (In milliseconds)
float temp;
float humidity;
unsigned long startTime;

const int pumpPins[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
bool pumpStatus[] = {LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW};


void setup() {

  THsensor.begin();

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

    //      $pump01
    if (command.charAt(0) == '$') { //Indicates pump
      int index = command.substring(5).toInt();
      index -= 1;
      togglePumps(index);

    } else if(command == "getTemp")
    {
      temp = THsensor.readTemperature();
      Serial.println("T: "+String(temp)); 
     
    } else if(command == "getHumid")
    {
      humidity = THsensor.readHumidity();
      Serial.println("H: "+String(humidity));
    }
    
    

  } 




}
