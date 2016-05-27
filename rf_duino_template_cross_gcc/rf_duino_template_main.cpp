#include "Arduino.h"
#include "RFduinoBLE.h"

void setup();
void loop();
//#line 1
#define SAMPLE_SIZE 64
#define FFT_SIZE SAMPLE_SIZE
#define IFFT_FLAG 0
#define BIT_REVERSE 0

//#define ARM_MATH_CM0
#include "arm_math.h"
#include "arm_common_tables.h"

int analogInPin = 3;

short int input[SAMPLE_SIZE];
short int output[FFT_SIZE];

bool data_received = false;

void calcul_fft() {

	arm_cfft_radix4_instance_q15 S_CFFT; /* ARM CFFT module */
	arm_rfft_instance_q15 S;

	for (int i = 0; i < SAMPLE_SIZE; i += 2) {
		input[i] = analogRead(analogInPin);
		input[i + 1] = 0;
	}

	/* Initialize the CFFT/CIFFT module, intFlag = 0, doBitReverse = 0 */
	//arm_cfft_radix4_init_q15(&S_CFFT, FFT_SIZE, IFFT_FLAG, BIT_REVERSE);
	/* Process the data through the CFFT/CIFFT module */
	//arm_cfft_radix4_q15(&S_CFFT, input);
	/* Process the data through the Complex Magnitude Module for calculating the magnitude at each bin */
	//arm_cmplx_mag_q15(input, output, FFT_SIZE);
	arm_rfft_init_q15(&S, &S_CFFT, FFT_SIZE, IFFT_FLAG, BIT_REVERSE);
	arm_rfft_q15(&S, input, output);

	/* Calculates maxValue and returns corresponding value */
	//arm_max_q15(output, FFT_SIZE, &maxValue, &maxIndex);
	//free(input);
	//return output;
}

void setup() {
	// this is the data we want to appear in the advertisement
	// (if the deviceName and advertisementData are too long to fix into the 31 byte
	// ble advertisement packet, then the advertisementData is truncated first down to
	// a single byte, then it will truncate the deviceName)
	//RFduinoBLE.advertisementData = "rf_duino_template";
	//RFduinoBLE.deviceName = "rf_duino";
	Serial.begin(9600);
	Serial.println("BEGIN...");
	RFduinoBLE.begin();
}

void loop() {
	Serial.println("LOOP...");
	/*RFduinoBLE.send(1);
	RFduinoBLE.send(2);
	RFduinoBLE.send(3);
	RFduinoBLE.send(4);*/

	//if (data_received) {
		calcul_fft();
	//}

	for (int i = 1; i < FFT_SIZE; i++) {
		//if (output[i] > 10) {
			//RFduinoBLE.sendInt(i);
			Serial.print("output[");
			Serial.print(i);
			Serial.print("] = ");
			Serial.println(output[i]);
		//}
	}

	/*static int count = 0;
	//RFduinoBLE.send("LOOP...", 8);
	//RFduinoBLE.send(count);
	//RFduinoBLE.sendInt(10*count);
	//RFduinoBLE.sendInt(100*count);
	count = (count + 1) % 1000;
	delay(100);*/
}

void RFduinoBLE_onReceive(char *data, int len) {
	data_received = true;
	Serial.println("some data received : ");
	Serial.print("0x");
	for (int bytePos = 0; bytePos < len; bytePos++) {
		Serial.print(" ");
		Serial.print((byte) data[bytePos], 16);
	}

}

