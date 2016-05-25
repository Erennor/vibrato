#include "Arduino.h"
#include "RFduinoBLE.h"

void setup();
void loop();
#line 1
#define SAMPLE_SIZE 128
#define FFT_SIZE SAMPLE_SIZE
#define IFFT_FLAG 0
#define BIT_REVERSE 0

//#define ARM_MATH_CM0
#include "arm_math.h"
#include "arm_common_tables.h"

int analogInPin = 3;

short int *calcul_fft() {

	short int *input = (short int *) malloc(SAMPLE_SIZE * sizeof(int));
	short int *output = (short int *) malloc(FFT_SIZE * sizeof(int));

	arm_cfft_radix4_instance_q15 S_CFFT; /* ARM CFFT module */
	arm_rfft_instance_q15 S;

	short int maxValue; /* Max FFT value is stored here */
	uint32_t maxIndex; /* Index in Output array where max value is */
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
	free(input);
	return output;

}

void setup() {
	Serial.begin(115200);
}

void loop() {
	// put your main code here, to run repeatedly:
	//Serial.println("LOOP...");
	//Serial.println((int) analogRead(analogInPin));
	short int *fft = calcul_fft();
	for (int i = 1; i < FFT_SIZE; i++) {
		if (fft[i] > 10) {
			Serial.print("fft[");
			Serial.print(i);
			Serial.print("] = ");
			Serial.println(fft[i]);
		}
	}
	free(fft);
}
