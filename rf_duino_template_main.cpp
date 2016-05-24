#include "Arduino.h"
#include "RFduinoBLE.h"

void setup();
void loop();
#line 1
void setup() {
	  Serial.begin(9600);
	  Serial.println("rf_duino_template_cross_gcc");

	  // this is the data we want to appear in the advertisement
	  // (if the deviceName and advertisementData are too long to fix into the 31 byte
	  // ble advertisement packet, then the advertisementData is truncated first down to
	  // a single byte, then it will truncate the deviceName)
	  RFduinoBLE.advertisementData = "rf_duino_template";
	  RFduinoBLE.deviceName = "rf_duino";

	  // start the BLE stack
	  RFduinoBLE.begin();
}

void loop() {
	static int count = 0;
	RFduinoBLE.send(count);
	count = (count + 1) % 1000;
	delay(100);
}

void RFduinoBLE_onReceive(char *data, int len)
{
	Serial.println("some data received : ");
	Serial.print("0x");
	for(int bytePos = 0; bytePos < len; bytePos++){
		Serial.print(" ");
		Serial.print((byte) data[bytePos], 16);
	}
}

