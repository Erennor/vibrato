import binascii
import struct
import numpy as np

import bluepy.btle as btle
from bluepy.btle import UUID, Peripheral, DefaultDelegate
from bluepy.btle import UUID, Peripheral
from tcp_listener import Listener
from hit_analyser import Analyser

listener = Listener(Analyser.cmd_handler)
listener.start_listening()


class MyDelegate(DefaultDelegate):

    def send_signal(self):
        #print(self.fft)
        #print (str(len(self.fft)))
        Analyser.analyse(self.fft)
        self.fft = [0] * 256
        self.current_index = 0


    def read_val(self, fft_input, index):
        """Read value from fft_input[index] to fft_input[index+4] and
            fill fft with detected value"""
        position = fft_input[index]
        if position < self.current_index:
            self.send_signal()
        for i in range(self.current_index, position):
            self.fft[i] = 0
        self.current_index = position
        val_reelle = fft_input[index + 1] + (fft_input[index + 2] << 8)
        val_img = fft_input[index + 3] + (fft_input[index + 4] << 8)
        if val_img > 60000:
            val_img = val_img - 65536
        self.fft[position] = val_reelle
        self.fft[position + 1] = val_img
        return

    def __init__(self):
        DefaultDelegate.__init__(self)
        self.current_index = 0
        self.fft = [0] * 256

    def handleNotification(self, cHandle, data):
        fft_input = binascii.b2a_hex(data)
        fft_input = binascii.unhexlify(fft_input)
        longueur = len(fft_input)
        fft_treated = []
        for i in range(0, 20):
            fft_treated.append(ord(fft_input[i]))

        for i in range(0, longueur, 5):
            self.read_val(fft_treated, i)

rx_uuid = UUID(0x2221)
sample_size = 128

# p = Peripheral("D9:35:6A:75:9F:9D", "random") # Rfduino sur usb
p = Peripheral("FE:CE:2E:0F:7D:51", "random")   # Rfduino sur pcb

p.withDelegate(MyDelegate())

print " device connected..."

try:
    p.getServices()
    ch = p.getCharacteristics(uuid=rx_uuid)[0]
    print ("notify characteristic with uuid 0x" + rx_uuid.getCommonName())
    cccid = btle.AssignedNumbers.client_characteristic_configuration
    # Ox000F : handle of Client Characteristic Configuration descriptor Rx - (generic uuid 0x2902)
    p.writeCharacteristic(0x000F, struct.pack('<bb', 0x01, 0x00), False)

    if ch.supportsRead():
        while 1:
            p.waitForNotifications(604800)  # 1 semaine d'attente
            # handleNotification() was called
            continue

finally:
    Analyser.ls.close()
    p.disconnect()
