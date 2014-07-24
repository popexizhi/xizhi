/*
 Chat  Server
 
 A simple server that distributes any incoming messages to all
 connected clients.  To use telnet to  your device's IP address and type.
 You can see the client's input in the serial monitor as well.
 Using an Arduino Wiznet Ethernet shield. 
 
 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 * Analog inputs attached to pins A0 through A5 (optional)
 
 created 18 Dec 2009
 by David A. Mellis
 modified 9 Apr 2012
 by Tom Igoe
 
 */

#include <SPI.h>
#include <Ethernet.h>

// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network.
// gateway and subnet are optional:
byte mac[] = { 
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192,168,1, 177);
IPAddress gateway(192,168,1, 1);
IPAddress subnet(255, 255, 0, 0);
const int _powerPin=13;    //the number for power pin  [add for popexihi]

// telnet defaults to port 23
EthernetServer server(23);
boolean alreadyConnected = false; // whether or not the client was connected previously

void setup() {
  // initialize the ethernet device
  Ethernet.begin(mac, ip, gateway, subnet);
  // start listening for clients
  server.begin();
  //initialise the power pin as an output
   pinMode(_powerPin,OUTPUT); 
 // Open serial communications and wait for port to open:
  Serial.begin(9600);
   while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }


  Serial.print("Chat server address:");
  Serial.println(Ethernet.localIP());
}
void _Openpower(){
 // add for popexizhi 
 // open power
digitalWrite(_powerPin,HIGH);
}
void _Closepower(){
// add for popexizhi
// close power
digitalWrite(_powerPin,LOW);
}
void loop() {
  // wait for a new client:
  EthernetClient client = server.available();

  // when the client sends the first byte, say hello:
  if (client) {
    if (!alreadyConnected) {
      // clead out the input buffer:
      client.flush();    
      Serial.println("We have a new client");
      client.println("Hello,arduino is ok!"); 
      alreadyConnected = true;
    } 

    if (client.available() > 0) {
      // read the bytes incoming from the client:
      char thisChar = client.read();
      //String getcon=String("open");
      String getcon = String(thisChar);
      // echo the bytes back to the client:
      server.write(thisChar);
      //process thisChar.string
      if (getcon== "open" ){
      //open power
      _Openpower();
      }
      if (getcon == "close"){
     //close power
      _Closepower();
      }
      // echo the bytes to the server as well:
      Serial.write(thisChar);
    }
  }
}
