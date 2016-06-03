#include "kiss_fft.h"
#include "Arduino.h"
#include "RFduinoBLE.h"
#include <Ai_RFD_WS2812.h>

#define SAMPLE_SIZE 128
#define SEUIL_DUREE 5   //valeur empirique

#define PIN 3
RFD_WS2812 blinker = RFD_WS2812(1, PIN);

const int analogInPin = 4; // Analog input pin that the potentiometer is attached to
int sensorValue;

kiss_fft_cpx cx_in[SAMPLE_SIZE];
kiss_fft_cpx cx_out[SAMPLE_SIZE];

char fft_input[20];   //20 octets

/**
   Return : duree du signal ou 0 si erreur
*/
long calcul_fft() {
  kiss_fft_cfg cfg = kiss_fft_alloc(SAMPLE_SIZE, 0, 0, 0);

  long t0 = micros();
  long t1 = 0;
  bool cal = false;
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    sensorValue = analogRead(analogInPin);
    //Serial.println(sensorValue);
    //delay(2);
    cx_in[i].r = sensorValue;
    cx_in[i].i = sensorValue;
    if (i > 5
        && abs(cx_in[i].r - cx_in[i - 3].r) < SEUIL_DUREE
        && abs(cx_in[i].r - cx_in[i - 2].r) < SEUIL_DUREE
        && abs(cx_in[i].r - cx_in[i - 1].r) < SEUIL_DUREE
        && !cal) {
      t1 = micros();
      cal = true;
    }
  }
  if (!cal) t1 = micros();

  kiss_fft( cfg , cx_in , cx_out );
  // transformed. DC is in cx_out[0].r and cx_out[0].i

  free(cfg);
  if (t1 != 0) return (t1 - t0);
  else return 0;
}

int min_sample(kiss_fft_cpx input[SAMPLE_SIZE]) {
  int mini = input[0].r;
  for (int i = 1; i < SAMPLE_SIZE; i++) {
    mini = min(mini, input[i].r);
  }
  return mini;
}

int max_sample(kiss_fft_cpx input[SAMPLE_SIZE]) {
  int maxi = input[0].r;
  for (int i = 1; i < SAMPLE_SIZE; i++) {
    maxi = max(maxi, input[i].r);
  }
  return maxi;
}

void setup() {
  //pinMode(pinLed, OUTPUT);
  Serial.begin(9600);
  //Serial.setDebugOutput(true);
  Serial.println("BEGIN...");
  RFduinoBLE.deviceName = "RFduino";
  RFduinoBLE.begin();

  // Initialize WS2812 modules with all LEDs turned off
  blinker.initialize();
  blinker.setPixel(0, blinker.packRGB(64, 0, 0));
  blinker.render();
}

void loop() {
  //Serial.println("LOOP...");
  //digitalWrite(pinLed, HIGH);
  long t = calcul_fft();
  //if (t > 1000) Serial.println(t);
  int j = 0;
  bool envoi = false;
  for (int i = 1; i < SAMPLE_SIZE; i++) {
    if (cx_out[i].r > 300) {   //valeur empirique

      blinker.setPixel(0, blinker.packRGB(0, 64, 0));
      blinker.render();
      //Envoi du max, min et duree
      /*if (!envoi) {
        Serial.println("LQ?QSJDOQSJFKLC?JQKLDJFVKLFSDJVKLD?VKL?KLSD?VKDS");
        int mini = min_sample(cx_in);
        int maxi = max_sample(cx_in);
        fft_input[0] = mini;
        fft_input[1] = mini >> 8;
        fft_input[2] = maxi;
        fft_input[3] = maxi >> 8;
        RFduinoBLE.send(fft_input, 4);
        envoi = true;
        }*/

      fft_input[j] = i;
      fft_input[j + 1] = cx_out[i].r;
      fft_input[j + 2] = cx_out[i].r >> 8;
      fft_input[j + 3] = cx_out[i].i;
      fft_input[j + 4] = cx_out[i].i >> 8;

      j = (j + 5) % 20;

      //On a remplit la trame au max, on l'envoi
      if (j == 0) {
        RFduinoBLE.send(fft_input, 20);
      }

      //On arrive au bout du tableau, on envoi ce qu'on a enregistré
      if (i == SAMPLE_SIZE - 1 && j != 0) {
        RFduinoBLE.send(fft_input, j);
      }

      Serial.print("fft[");
      Serial.print(i);
      Serial.print("] = ");
      Serial.print(cx_out[i].r);
      Serial.print("  ");
      Serial.println(cx_out[i].i);
    }
  }
  blinker.setPixel(0, blinker.packRGB(64, 0, 0));
  blinker.render();
  //delay(1000);
}

void RFduinoBLE_onReceive(char *data, int len) {
  Serial.println("some data received : ");
  Serial.print("0x");
  for (int bytePos = 0; bytePos < len; bytePos++) {
    Serial.print(" ");
    Serial.print((byte) data[bytePos], 16);
  }

}
