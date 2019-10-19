//无力模式读数据

#include <ArduinoJson.h>
#include<Arm7Bot.h>
Arm7Bot arm;

String json = "";
int data[7];

void setup() {
  arm.init();
  for(int i = 0 ;i < 7;i++){
    arm.setServoTorque(i,2);
  }
}

void loop() {
    read();
}
void  read() {
  for(int i =0 ;i <7 ;i ++){
    data[i]=arm.readServoPos(i);
  }
  send();
  delay(1000);
}
bool send() {
  DynamicJsonBuffer jsonBuffer;
  JsonObject& root1 = jsonBuffer.createObject();
  
  root1["0"] = data[0];
  root1["1"] = data[1];
  root1["2"] = data[2];
  root1["3"] = data[3];
  root1["4"] = data[4];
  root1["5"] = data[5];
  root1["6"] = data[6];
  String json2;
  root1.printTo(json2);
  Serial.println(json2);
}
