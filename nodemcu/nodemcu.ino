#define MAX_SRV_CLIENTS 3
#define SAMPLE_SIZE 256

#include <ESP8266WiFi.h>
#include "kiss_fft.h"

const char* ssid = "ssid";
const char* password = "xxxxxxxxxx";

WiFiServer server(21);
WiFiClient serverClients[MAX_SRV_CLIENTS];

const int analogInPin = A0; // Analog input pin that the potentiometer is attached to

kiss_fft_cpx *fft;

kiss_fft_cpx * calcul_fft() {
  kiss_fft_cfg cfg = kiss_fft_alloc(SAMPLE_SIZE, 0, 0, 0);
  kiss_fft_cpx *cx_in = (kiss_fft_cpx*)malloc(SAMPLE_SIZE * sizeof(kiss_fft_cpx));
  kiss_fft_cpx *cx_out = (kiss_fft_cpx*)malloc(SAMPLE_SIZE * sizeof(kiss_fft_cpx));

  for (int i = 0; i < SAMPLE_SIZE; i++) {
    cx_in[i].r = analogRead(analogInPin);
    cx_in[i].i = 0;
  }

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
      //data sent to the connected clients
      fft = calcul_fft();
      for (int k = 0; k < SAMPLE_SIZE; k++) {
        serverClients[i].println(fft[k].r);
      }
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
