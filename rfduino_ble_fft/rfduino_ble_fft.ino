//#define FIXED_POINT 32
#define kiss_fft_scalar int

#include "kiss_fft.h"
#include "Arduino.h"
#include "RFduinoBLE.h"
#include <Ai_RFD_WS2812.h>

#define SAMPLE_SIZE 128

#define PIN 3
RFD_WS2812 blinker = RFD_WS2812(1, PIN);
bool led = false;

const int analogInPin = 4; // Analog input pin that the potentiometer is attached to
int sensorValue;
bool debutCalcul = true;
bool finCalcul = false;

kiss_fft_cpx cx_in[SAMPLE_SIZE];
kiss_fft_cpx cx_out[SAMPLE_SIZE];

char fft_input[20];   //20 octets

unsigned long valeur_seuil = 0;
unsigned int coeff_seuil = 700;
bool coup_detecte = false;

unsigned int valeur_abs(int val) {
  if (val < 0) return (-1) * val;
  else return val;
}

/**
   Renvoi l'écart moyen d'une mesure
*/
unsigned long ecart_moyen() {
  blinker.setPixel(0, blinker.packRGB(0, 0, 255));
  blinker.render();
  Serial.println("calibrage...");
  delay(5000);
  unsigned long moyenne = 0;
  unsigned long ecart_moyen = 0;
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    sensorValue = analogRead(analogInPin);
    moyenne = moyenne + sensorValue;
    //Serial.println(sensorValue);
    cx_in[i].r = sensorValue;
    cx_in[i].i = sensorValue;
  }
  moyenne = moyenne / SAMPLE_SIZE;
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    ecart_moyen = ecart_moyen + valeur_abs(cx_in[i].r - moyenne);
  }
  ecart_moyen = ecart_moyen / SAMPLE_SIZE;
  blinker.setPixel(0, blinker.packRGB(255, 0, 0));
  blinker.render();
  return ecart_moyen;
}

/**
   Renvoi une valeur seuil pour la reconnaissance des coups
*/
unsigned int calcul_coeff_seuil() {
  blinker.setPixel(0, blinker.packRGB(0, 0, 255));
  blinker.render();
  unsigned long moyenneR = 0;
  unsigned long moyenneI = 0;
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    sensorValue = analogRead(analogInPin);
    //Serial.println(sensorValue);
    cx_in[i].r = sensorValue;
    cx_in[i].i = sensorValue;
  }
  calcul_fft();
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    //Probleme de signe...
    cx_out[i].r = cx_out[i].r & 0x7FFFFFFF;
    cx_out[i].i = cx_out[i].i & 0x7FFFFFFF;
  }
  for (int i = 6; i < SAMPLE_SIZE - 4; i++) {
    moyenneR = moyenneR + cx_out[i].r;
    moyenneI = moyenneI + cx_out[i].i;
  }

  moyenneR = moyenneR / (SAMPLE_SIZE - 10);
  moyenneI = moyenneI / (SAMPLE_SIZE - 10);
  Serial.println("moyennes de fft : ");
  Serial.println(moyenneR);
  Serial.println(moyenneI);
  int mini = min_sample(cx_out);
  int maxi = max_sample(cx_out);
  Serial.println(mini);
  Serial.println(maxi);

  blinker.setPixel(0, blinker.packRGB(64, 0, 0));
  blinker.render();
  return 5 * (moyenneR);
}

/**
   Return : duree du signal ou 0 si erreur
*/
long calcul_fft() {
  kiss_fft_cfg cfg = kiss_fft_alloc(SAMPLE_SIZE, 0, 0, 0);

  long t0 = micros();
  long t1 = 0;
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    sensorValue = analogRead(analogInPin);
    //Serial.println(sensorValue);
    cx_in[i].r = sensorValue;
    cx_in[i].i = sensorValue;
    if (i > 10
        && valeur_abs(cx_in[i].r - cx_in[i - 10].r) < valeur_seuil
        && valeur_abs(cx_in[i].r - cx_in[i - 9].r) < valeur_seuil
        && valeur_abs(cx_in[i].r - cx_in[i - 8].r) < valeur_seuil
        && valeur_abs(cx_in[i].r - cx_in[i - 7].r) < valeur_seuil
        && valeur_abs(cx_in[i].r - cx_in[i - 6].r) < valeur_seuil
        && valeur_abs(cx_in[i].r - cx_in[i - 5].r) < valeur_seuil
        && valeur_abs(cx_in[i].r - cx_in[i - 4].r) < valeur_seuil
        && valeur_abs(cx_in[i].r - cx_in[i - 3].r) < valeur_seuil
        && valeur_abs(cx_in[i].r - cx_in[i - 2].r) < valeur_seuil
        && valeur_abs(cx_in[i].r - cx_in[i - 1].r) < valeur_seuil
        && !finCalcul) {
      t1 = micros();
      finCalcul = true;
    }
  }
  if (!finCalcul) t1 = micros();

  kiss_fft( cfg , cx_in , cx_out );
  // transformed. DC is in cx_out[0].r and cx_out[0].i

  free(cfg);
  if (t1 != 0) return (t1 - t0);
  else return 0;
}

int min_sample(kiss_fft_cpx input[SAMPLE_SIZE]) {
  int mini = input[6].r;
  for (int i = 6; i < SAMPLE_SIZE - 4; i++) {
    mini = min(mini, input[i].r);
  }
  return mini;
}

int max_sample(kiss_fft_cpx input[SAMPLE_SIZE]) {
  int maxi = input[6].r;
  for (int i = 6; i < SAMPLE_SIZE - 4; i++) {
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
  valeur_seuil = ecart_moyen();
  //coeff_seuil = calcul_coeff_seuil();
  Serial.print("Seuil : ");
  Serial.println(coeff_seuil);
}

void loop() {
  //Serial.println("LOOP...");
  long t = calcul_fft();
  //if (t > 1000) Serial.println(t);
  int j = 0;
  long t1 = 0;
  coup_detecte = false;
  for (int i = 6; i < SAMPLE_SIZE - 4; i++) {

    //Probleme de signe...
    cx_out[i].r = cx_out[i].r & 0x7FFFFFFF;
    cx_out[i].i = cx_out[i].i & 0x7FFFFFFF;

    if (cx_out[i].r > coeff_seuil) {   //valeur empirique
      coup_detecte = true;
      //Serial.println(i);
      if (debutCalcul) {
        //RFduinoBLE.sendByte(255);
        //Serial.println(255);
        debutCalcul = false;
      }

      blinker.setPixel(0, blinker.packRGB(0, 64, 0));
      blinker.render();
      if (!led) {
        t1 = millis();
        led = true;
      }

      fft_input[j] = i;
      fft_input[j + 1] = cx_out[i].r;
      fft_input[j + 2] = cx_out[i].r >> 8;
      fft_input[j + 3] = cx_out[i].i;
      fft_input[j + 4] = cx_out[i].i >> 8;

      j = (j + 5) % 20;

      //On a remplit la trame au max, on l'envoi
      if (j == 0) {
        RFduinoBLE.send(fft_input, 20);
        //Serial.println("Envoi d'une trame de taille 20");
      }

      Serial.print("fft[");
      Serial.print(i);
      Serial.print("] = ");
      Serial.print(cx_out[i].r);
      Serial.print("  ");
      Serial.println(cx_out[i].i);

    }
    //On arrive au bout du tableau, on envoi ce qu'on a enregistré
    if (i == SAMPLE_SIZE - 1 && j != 0) {
      for (int k = j; k < 20; k++) {
        fft_input[k] = 0;
      }
      RFduinoBLE.send(fft_input, 20);
      //Serial.println("Envoi d'un tableau complété de 0");
    }
    if (i == SAMPLE_SIZE - 1 && coup_detecte) {
      for (int k = 0; k < 20; k++) {
        fft_input[k] = 0;
      }
      RFduinoBLE.send(fft_input, 20);
      //Serial.println("Fin de tableau");
    }
  }
  //Tout le signal a été calculé, on envoi un octet de 0 pour signaler la fin du signal
  if (finCalcul && !debutCalcul) {
    //RFduinoBLE.sendByte(0);
    //Serial.println(0);
    finCalcul = false;
    debutCalcul = true;
  }

  long t2 = millis();
  if (t2 - t1 > 3000) {
    t1 = 0;
    t2 = 0;
    blinker.setPixel(0, blinker.packRGB(64, 0, 0));
    blinker.render();
    led = false;
  }
}

void RFduinoBLE_onReceive(char *data, int len) {
  Serial.println("some data received : ");
  Serial.print("0x");
  for (int bytePos = 0; bytePos < len; bytePos++) {
    Serial.print(" ");
    Serial.print((byte) data[bytePos], 16);
  }

}
