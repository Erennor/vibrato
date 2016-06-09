#include "kiss_fftr.h"
#include "Arduino.h"
#include "RFduinoBLE.h"
#include <Ai_RFD_WS2812.h>

#define PIN 3
RFD_WS2812 blinker = RFD_WS2812(1, PIN);

const int analogInPin = 4; // Analog input pin that the potentiometer is attached to
int sensorValue;

char fft_input[20];   //20 octets

bool coup_detecte = false;

unsigned long valeur_seuil = 50;
unsigned long valeur_ecart = 0;
const unsigned long sample_size = 256;
const unsigned long fft_size = 128;

kiss_fft_scalar cx_in[sample_size];
kiss_fft_cpx cx_out[fft_size];

unsigned int valeur_abs(int val) {
  if (val < 0) return (-1) * val;
  else return val;
}

/**
   Renvoi la moyenne d'un echantillon de taille sample_size
*/
unsigned long moyenne(kiss_fft_scalar input[sample_size]) {
  unsigned long moyenne = 0;
  for (int i = 0; i < sample_size; i++) {
    moyenne = moyenne + input[i];
    //Serial.println(sensorValue);
  }
  moyenne = moyenne / sample_size;
  return moyenne;
}

void calibrage() {
  blinker.setPixel(0, blinker.packRGB(0, 0, 255));
  blinker.render();
  Serial.println("Calibrage...");
  delay(2000);
  for (int i = 0; i < sample_size; i++) {
    sensorValue = analogRead(analogInPin);
    //Serial.println(sensorValue);
    cx_in[i] = sensorValue;
  }
  valeur_ecart = moyenne(cx_in);
  //valeur_ecart = ecart_moyen(cx_in);
  //Serial.println(valeur_seuil);
  Serial.print("Valeur moyenne : ");
  Serial.println(valeur_ecart);
  blinker.setPixel(0, blinker.packRGB(255, 0, 0));
  blinker.render();
}

void calcul_fft() {
  kiss_fftr_cfg cfg = kiss_fftr_alloc(sample_size, 0, 0, 0);
  kiss_fftr( cfg , cx_in , cx_out );
  free(cfg);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //Serial.setDebugOutput(true);
  RFduinoBLE.deviceName = "RFduino";
  RFduinoBLE.begin();

  // Initialize WS2812 modules with all LEDs turned off
  blinker.initialize();
  calibrage();
}

void loop() {
  // put your main code here, to run repeatedly:
  while (!coup_detecte) {
    sensorValue = analogRead(analogInPin);
    //Serial.println(sensorValue);
    if (valeur_abs(valeur_ecart - sensorValue) > valeur_seuil) {
      coup_detecte = true;
      Serial.println("COUP DETECTE !");
      //Serial.println(valeur_ecart);
    }
  }
  blinker.setPixel(0, blinker.packRGB(0, 255, 0));
  blinker.render();

  //long t0 = millis();
  for (int i = 0; i < sample_size; i++) {
    sensorValue = analogRead(analogInPin);
    delayMicroseconds(100);
    cx_in[i] = sensorValue;
  }
  //long t1 = millis();
  //Serial.print("TEMPS : ");
  //Serial.println(t1-t0);
  
  calcul_fft();

  //Affichage des valeurs pour debug
  /*for (int i = 1; i < fft_size; i += 2) {
    Serial.print("fft[");
    Serial.print(i);
    Serial.print("] = ");
    //Serial.print(cx_out[i].r);
      Serial.print(" ");
      Serial.print((int) cx_out[i].r);
      Serial.print("    ");
      // Serial.print(cx_out[i].i);
      Serial.print(" ");
      Serial.print((int) cx_out[i].i);

    for (int j = 0; j < (valeur_abs(cx_out[i].i) + valeur_abs(cx_out[i + 1].i)) / 50; j++) {
      Serial.print("#");
    }
    Serial.println();
    Serial.print("fft[i] = ");
    for (int j = 0; j < (valeur_abs(cx_out[i].r) + valeur_abs(cx_out[i + 1].r)) / 50; j++) {
      Serial.print("#");
    }
    Serial.println();
    }*/

  //Envoi de la fft par BLE
  for (int i = 0; i < fft_size / 4; i++) {
    for (int j = 0; j < 4; j++) {
      fft_input[5 * j] = (char) (4 * i) + j;
      //Serial.println((int)fft_input[5 * j]);
      fft_input[5 * j + 1] = (char)(((int) cx_out[4 * i + j].r) % 256);
      fft_input[5 * j + 2] = (char)((((int) cx_out[4 * i + j].r) >> 8) % 256);
      //Serial.println(((((int)fft_input[5 * j + 2]) << 8) + (int)fft_input[5 * j + 1]) & 0x3FFF);
      fft_input[5 * j + 3] = (char)(((int) cx_out[4 * i + j].i) % 256);
      fft_input[5 * j + 4] = (char)((((int) cx_out[4 * i + j].i) >> 8) % 256);
      //Serial.println((((int)fft_input[5 * j + 4]) << 8) + (int)fft_input[5 * j + 3]);
      /*for (int k = 0; k < (((((int)fft_input[5 * j + 2]) << 8) + (int)fft_input[5 * j + 1]) & 0x7FFF) / 10; k++) {
        Serial.print('#');
        }
        Serial.println();*/
    }
    RFduinoBLE.send(fft_input, 20);
    delay(30);
  }
  //Serial.println();
  //Envoi d'un tableau de 0 pour marquer la fin de l'envoi
  for (int i = 0; i < 20; i++) {
    fft_input[i] = 0;
  }
  RFduinoBLE.send(fft_input, 20);

  coup_detecte = false;
  blinker.setPixel(0, blinker.packRGB(255, 0, 0));
  blinker.render();
}



void RFduinoBLE_onReceive(char *data, int len) {
  calibrage();
}















