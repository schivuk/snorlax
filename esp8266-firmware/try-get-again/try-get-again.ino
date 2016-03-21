/*
 *  This sketch sends data via HTTP GET requests to a web server.
 *  
 *  Verify WiFi works correctly
 *
 */

#include <ESP8266WiFi.h>

const char* ssid = "CMU";
//This is actually my laptop running the snorlax server. Replace it
// with the IP of the server of your choice
const char* host = "128.237.170.104";

void setup() {
  Serial.begin(115200);
  delay(10);


  //loop to allow time for the user to open and setup Serial monitor
  for(int i=0; i<10; i++) {
    Serial.println("Hello, testing serial over here");
    Serial.println(i);
    delay(500);
  }
  // We start by connecting to a WiFi network

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

int value = 0;

void loop() {
  delay(5000);
  ++value;

  Serial.print("connecting to ");
  Serial.println(host);
  
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 8000;
  while(!client.connect(host, httpPort)) {
    Serial.println("connection failed, retrying..");
    delay(500);
  }
  
  // We now create a URI for the request
  String url = "/storeData";
  
  Serial.print("Requesting URL: ");
  Serial.println(url);
  
  //Generate a telnet-like request
  StringSumHelper request = String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n\r\n";

  Serial.println(request);
  // This will send the request to the server
  client.print(request);
  delay(10);
  
  // Read all the lines of the reply from server and print them to Serial
  while(client.available()){
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }
  
  Serial.println();
  Serial.println("closing connection");
}

