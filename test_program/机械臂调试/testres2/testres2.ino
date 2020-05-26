//串口发送各个机械臂舵机数据控制
//金色机械臂：黑色->GND；白色->18(rx)；灰色->19(tx)
//蓝色机械臂：


#include<HardwareSerial.h>
#include <ArduinoJson.h>
#include<Arm7Bot.h>
HardwareSerial orderSerial(1);
Arm7Bot arm;

String json = "";
int data[7];
int initt[7]={512,450,680,512,512,512};

void setup() {
  // put your setup code here, to run once:
  arm.init();
  //  Serial.begin(9600);
  orderSerial.begin(115200, SERIAL_8N1, 18, 19);//18,19引脚分别充当软串口的rx,tx
}

void loop() {
  // put your main code here, to run repeatedly:
  if (receive()) {
    decodeJson();
//    Serial.println(json);
  }
}
void  decodeJson() {
  DynamicJsonBuffer jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(json);
  if (!root.success()) {
    Serial.println("parseObject() failed");
    return;
  }
  data[0]=root["0"];
  data[1]=root["1"];
  data[2]=root["2"];
  data[3]=root["3"];
  data[4]=root["4"];
  data[5]=root["5"];
//  data[6]=root["6"];
  for(int i =0 ;i <6 ;i ++){
    Serial.println(data[i]);
    arm.setServoPos(i,data[i]);
  }
  delay(2500);
  for(int i =0 ;i <6 ;i ++){
    arm.setServoPos(i,initt[i]);
  }
}



bool receive() {

  bool op = 0;
  while (orderSerial.available() > 0)
  {
    if (!op) {
      json = "";
    }
    json += char(orderSerial.read());
    delayMicroseconds(1200);
    op = 1;
  }

  return op;
}
