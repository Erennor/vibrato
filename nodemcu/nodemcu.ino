#define MAX_SRV_CLIENTS 3
#define SAMPLE_SIZE 256

#include <ESP8266WiFi.h>
#include "kiss_fft.h"

const char* ssid = "A4H_creativity_lab";
const char* password = "Toutes ces machines pour fabriquer!";

//const char* ssid = "Moulinsart";
//const char* password = "A1B2C3D4E5";

WiFiServer server(21);
WiFiClient serverClients[MAX_SRV_CLIENTS];

const int analogInPin = A0; // Analog input pin that the potentiometer is attached to

kiss_fft_cpx * calcul_fft() {
  kiss_fft_cfg cfg = kiss_fft_alloc(SAMPLE_SIZE, 0, 0, 0);
  kiss_fft_cpx *cx_in = (kiss_fft_cpx*)malloc(SAMPLE_SIZE * sizeof(kiss_fft_cpx));
  kiss_fft_cpx *cx_out = (kiss_fft_cpx*)malloc(SAMPLE_SIZE * sizeof(kiss_fft_cpx));

  long t3;
  long t4;
  long t1 = micros();
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    t3 = micros();
    cx_in[i].r = analogRead(analogInPin);
    t4 = micros();
    cx_in[i].i = 0;
  }
  long t2 = micros();
  Serial.print("TEMPS SAMPLE_SIZE analogRead : ");
  Serial.println(t2 - t1);
  Serial.print("TEMPS 1 analogRead : ");
  Serial.println(t4 - t3);

  kiss_fft( cfg , cx_in , cx_out );
  // transformed. DC is in cx_out[0].r and cx_out[0].i

  free(cfg);
  free(cx_in);
  return cx_out;
}

void setup() {
  Serial.begin(115200);
  //Serial1.setDebugOutput(true);
  Serial.print("\nConnecting to "); Serial.println(ssid);
  WiFi.begin(ssid, password);
  uint8_t i = 0;
  while (WiFi.status() != WL_CONNECTED && i++ < 20) delay(500);
  if (i == 21) {
    Serial.print("Could not connect to"); Serial.println(ssid);
    while (1) delay(500);
  }
  //Serial.begin(115200);
  server.begin();
  server.setNoDelay(true);
  Serial.print("Ready! Use 'telnet ");
  Serial.print(WiFi.localIP());
  Serial.println(" 21' to connect");
}

void loop() {
  //Serial.println("LOOP...");
  uint8_t i;
  if (server.hasClient()) {
    for (i = 0; i < MAX_SRV_CLIENTS; i++) {
      if (!serverClients[i] || !serverClients[i].connected()) {
        if (serverClients[i]) serverClients[i].stop();
        serverClients[i] = server.available();
        continue;
      }
    }
    //no free spot
    WiFiClient serverClient = server.available();
    serverClient.stop();
  }
  for (i = 0; i < MAX_SRV_CLIENTS; i++) {
    if (serverClients[i] && serverClients[i].connected()) {
      //you can reply to the client here
      //serverClients[i].write("coucou");
      /*sensorValue = analogRead(analogInPin);
        serverClients[i].println(sensorValue);*/
      long t1 = micros();
      kiss_fft_cpx *fft = calcul_fft();
      long t2 = micros();
      Serial.print("TEMPS appel fonction ");
      Serial.println(t2 - t1);
      /*for (int k = 0; k < SAMPLE_SIZE; k++) {
        serverClients[i].print("fft[");
        serverClients[i].print(k);
        serverClients[i].print("] = ");
        serverClients[i].print(fft[k].r);
        serverClients[i].print("  ");
        serverClients[i].println(fft[k].i);
        }*/
      free(fft);
    }
  }
  /*if (Serial.available()) {
    size_t len = Serial.available();
    uint8_t sbuf[len];
    Serial.readBytes(sbuf, len);
    //bello is a broadcast to all clients
    for (i = 0; i < MAX_SRV_CLIENTS; i++) {
      if (serverClients[i] && serverClients[i].connected()) {
        serverClients[i].write(sbuf, len);
        delay(1);
      }
    }
    }*/
}
