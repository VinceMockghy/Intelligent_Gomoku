//接收下棋点测试

#include<HardwareSerial.h>
#include <ArduinoJson.h>
#include<Arm7Bot.h>
HardwareSerial orderSerial(1);

String json = "";

int set = 0;
int get1[6] = {295, 522, 451, 516, 357, 504};//获取棋子位置
int get0[6] = {512, 450, 680, 512, 512, 512};//机械臂初始位置
int data[6] = {644, 566, 478, 519, 375, 499};
int photo[6] = {523, 26, 740, 516, 170, 504};

Arm7Bot arm;

void setup() {
  // put your setup code here, to run once:
  arm.init();

  orderSerial.begin(115200, SERIAL_8N1, 18, 19);//18,19引脚分别充当软串口的rx,tx

  delay(1000);
  for (int i = 0; i < 7; i++) {
    arm.setServoSpeed(i, 400);
  }
  delay(2000);
  for (int i = 0 ; i < 6; i++) {
    arm.setServoPos(i, photo[i]);
  }
}


void loop() {
  // put your main code here, to run repeatedly:
  if (receive()) {
    decodeJson();
    move();
  }
}
void  decodeJson() {
  DynamicJsonBuffer jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(json);
  if (!root.success()) {
    Serial.println("parseObject() failed");
    return;
  }
  set = root["set"];
  data[0] = root["0"];
  data[1] = root["1"];
  data[2] = root["2"];
  data[3] = root["3"];
  data[4] = root["4"];
  data[5] = root["5"];

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

bool move() {
  for (int i = 0 ; i < 6; i++) {
    arm.setServoPos(i, get0[i]);
  }
  delay(4000);
  for (int i = 0 ; i < 6; i++) {
    arm.setServoPos(i, get1[i]);
  }
  delay(3000);
  arm.vacuum(true);
  delay(3000);
  for (int i = 0 ; i < 6; i++) {
    arm.setServoPos(i, get0[i]);
  }
  delay(4000);
  for (int i = 0 ; i < 6; i++) {
    arm.setServoPos(i, data[i]);
  }
  delay(4000);
  arm.vacuum(false);
  delay(3000);
  for (int i = 0 ; i < 6; i++) {
    arm.setServoPos(i, photo[i]);
  }
}
