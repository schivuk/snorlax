#include <SPI.h>
#include <ESP8266WiFi.h>

//Program to print the MAC address of the ESP chip

int status = WL_IDLE_STATUS;     // the Wifi radio's status

byte mac[6];                     // the MAC address of your Wifi shield


void setup()
{
 Serial.begin(115200);

 
  for(int i=0; i<10; i++) {
    Serial.println("Hello, testing serial over here");
    Serial.println(i);
    delay(500);
  }

  
  Serial.println("Getting mac addr:");
  WiFi.macAddress(mac);
  Serial.print("MAC: ");
  Serial.print(mac[0],HEX);
  Serial.print(":");
  Serial.print(mac[1],HEX);
  Serial.print(":");
  Serial.print(mac[2],HEX);
  Serial.print(":");
  Serial.print(mac[3],HEX);
  Serial.print(":");
  Serial.print(mac[4],HEX);
  Serial.print(":");
  Serial.println(mac[5],HEX);
 
}

void loop () {}
