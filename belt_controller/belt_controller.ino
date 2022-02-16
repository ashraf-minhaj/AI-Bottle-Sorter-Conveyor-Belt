#include <Servo.h>

int proximity_sensor_pin = 4;
int motor1 = 6;

Servo kicker;

void setup() {
  // put your setup code here, to run once:
  pinMode(motor1, OUTPUT);
  
  kicker.attach(2);
  kicker.write(180);
  
  Serial.begin(9600);
}

void belt_on(){
  digitalWrite(motor1, HIGH);
}

void belt_stop(){
  digitalWrite(motor1, LOW);
}

void send_master_to_analyze(){
  Serial.println('1');
}

void get_master_command(){
  byte data = " ";
  // the master computer will send data upon detection
    if (Serial.available() > 0) {
    // read the incoming byte:
    data = Serial.read();
    Serial.println(data);
    
    if (data == 'b'){
      // kicking bottle
      //digitalWrite(led_pin, HIGH);
      kicker.write(0);
      delay(500);
      return;
    }
    else if (data == 'n'){
      belt_on();
      delay(600);
      return;
    }
  }
  else{
    get_master_command();
  }
}

void loop() {
  // put your main code here, to run repeatedly:

  if (!digitalRead(proximity_sensor_pin)){
    belt_stop();
    send_master_to_analyze();
    get_master_command();
  }
  else{
    belt_on();
    kicker.write(180);
  }

  delay(100);
}
