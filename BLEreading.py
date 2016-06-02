import binascii
import struct
import numpy as np
from bluepy.btle import UUID, Peripheral

rx_uuid = UUID(0x2221)
sample_size = 128
fft = np.arange(0, 2*sample_size)

p = Peripheral("D9:35:6A:75:9F:9D", "random") # Rfduino sur usb
# p = Peripheral("FE:CE:2E:0F:7D:51", "random")   # Rfduino sur pcb

try:
    ch = p.getCharacteristics(uuid=rx_uuid)[0]
    if (ch.supportsRead()):
        print "Connected..."
        while 1:
            p.waitForNotifications(604800)  # 1 semaine d'attente
            print "Notification received..."

            fft_input = binascii.b2a_hex(ch.read())
            fft_input = binascii.unhexlify(fft_input)

            longueur = len(fft_input)
            #print longueur
            mini = 0
            maxi = 0

            if longueur == 4:
                mini = ord(fft_input[0]) + (ord(fft_input[1]) << 8)
                maxi = ord(fft_input[2]) + (ord(fft_input[3]) << 8)

            if longueur > 4:
                indice0 = ord(fft_input[0])
                valReelle0 = ord(fft_input[1]) + (ord(fft_input[2]) << 8)
                valIm0 = ord(fft_input[3]) + (ord(fft_input[4]) << 8)
                if valIm0 > 60000:
                    valIm0 = valIm0 - 65536

            if longueur > 5:
                indice1 = ord(fft_input[5])
                valReelle1 = ord(fft_input[6]) + (ord(fft_input[7]) << 8)
                valIm1 = ord(fft_input[8]) + (ord(fft_input[9]) << 8)
                if valIm1 > 60000:
                    valIm1 = valIm1 - 65536

            if longueur > 10:
                indice2 = ord(fft_input[10])
                valReelle2 = ord(fft_input[11]) + (ord(fft_input[12]) << 8)
                valIm2 = ord(fft_input[13]) + (ord(fft_input[14]) << 8)
                if valIm2 > 60000:
                    valIm2 = valIm2 - 65536

            if longueur > 15:
                indice3 = ord(fft_input[15])
                valReelle3 = ord(fft_input[16]) + (ord(fft_input[17]) << 8)
                valIm3 = ord(fft_input[18]) + (ord(fft_input[19]) << 8)
                if valIm3 > 60000:
                    valIm3 = valIm3 - 65536

            if mini != 0:
                print "min = " + str(mini)
            if maxi != 0:
                print "max = " + str(maxi)
            print "fft[" + str(indice0) + "] = " + str(valReelle0) + "  " + str(valIm0)
            print "fft[" + str(indice1) + "] = " + str(valReelle1) + "  " + str(valIm1)
            print "fft[" + str(indice2) + "] = " + str(valReelle2) + "  " + str(valIm2)
            print "fft[" + str(indice3) + "] = " + str(valReelle3) + "  " + str(valIm3)

            # Les coefficients reels sont sur les indices pairs
            # Les coefficients imaginaires sont sur les indices impairs
            fft[indice0] = valReelle0
            fft[indice0 + 1] = valIm0

            fft[indice1] = valReelle1
            fft[indice1 + 1] = valIm1

            fft[indice2] = valReelle2
            fft[indice2 + 1] = valIm2

            fft[indice3] = valReelle3
            fft[indice3 + 1] = valIm3

finally:
    p.disconnect()
