import binascii
import struct
import numpy as np
from matplotlib.backends.backend_pdf import fill

import bluepy.btle as btle
from bluepy.btle import UUID, Peripheral, DefaultDelegate
from bluepy.btle import UUID, Peripheral
from tcp_listener import Listener
from hit_analyser import Analyser

listener = Listener(Analyser.cmd_handler)
listener.start_listening()


class MyDelegate(DefaultDelegate):
    def send_signal(self):
        """Send received fft to controller"""
        Analyser.analyse(self.dft)
        self.dft = [0] * 256
        self.current_index = 0

    def fill(self, fft_input, index, position):
        """ fill dft with ff input from [fft_input[index + 1] .. fft_input[index + 4 ] """
        self.current_index = position + 2
        val_reelle = fft_input[index + 1] + (fft_input[index + 2] << 8)
        val_img = fft_input[index + 3] + (fft_input[index + 4] << 8)
        if val_img > 60000:
            val_img -= 65536
        if val_reelle > 60000:
            val_reelle -= 65536
        self.dft[position] = val_reelle
        self.dft[position + 1] = val_img

    def read_val(self, dft_input, index):
        """Read value from fft_input[index] to fft_input[index+4] and
            fill fft with detected value"""
        position = dft_input[index] * 2
        if position == 0:
            # might be the end of a signal, the beginning of a signal or 0's array
            if self.current_index > 2:
                # position is null : end of current fft array, send signal to controller
                if self.current_index != 256:
                    print "sending signal, but self.current_index = " + str(self.current_index)
                    print "some values were lost"
                self.send_signal()
                return
            else:
                # multiple 0 values can follow, this should caught these
                self.fill(dft_input, index, position)
        # In any other case, self.current_index should be equal to position
        elif position < self.current_index:
            # Should not happen, loss of value, end of array
            print ("Erreur , current index" + str(self.current_index) +
                   " inferieur a position " + str(position) + " mais non nul.")
            print ("Erreur , loss of values")
            self.send_signal()
            self.fill(dft_input, index, position)
        elif position > self.current_index:
            # Some values were lost
            print("position = " + str(position) + " current index = " + str(self.current_index))
            print "Erreur, some  value were lost, auto filling with 0"
            self.fill(dft_input, index, position)
        else:
            self.fill(dft_input, index, position)

    def __init__(self):
        DefaultDelegate.__init__(self)
        self.current_index = 0
        self.dft = [0] * 256

    def handleNotification(self, cHandle, data):
        # convert data to readable integer
        fft_input = binascii.b2a_hex(data)
        fft_input = binascii.unhexlify(fft_input)
        longueur = len(fft_input)
        dft_treated = []
        for i in range(0, 20):
            dft_treated.append(ord(fft_input[i]))
        for i in range(0, longueur, 5):
            self.read_val(dft_treated, i)


rx_uuid = UUID(0x2221)
sample_size = 128
# p = Peripheral("D9:35:6A:75:9F:9D", "random") # Rfduino sur usb
p = Peripheral("FE:CE:2E:0F:7D:51", "random")  # Rfduino sur pcb
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
