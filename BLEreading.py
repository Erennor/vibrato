import binascii
import struct
import numpy as np
from bluepy.btle import UUID, Peripheral

rx_uuid = UUID(0x2221)
sample_size = 128
fft = np.arange(0, 2 * sample_size)

p = Peripheral("d9:35:6a:75:9f:9d", "random")

# Recupere les 12 bits de poids fort
def getIndice(int32):
    return int32 >> 20

# Recupere les bits 10-19
def getReelle(int32):
    return (int32 & 0xFFC00) >> 10

# Recupere les 10 bits de poids faible
def getIm(int32):
    return int32 & 0x3FF


try:
    ch = p.getCharacteristics(uuid=rx_uuid)[0]
    if (ch.supportsRead()):
        while 1:
            p.waitForNotifications(10)

            fft_input = binascii.b2a_hex(ch.read())
            fft_input = binascii.unhexlify(fft_input)
            fft_input = struct.unpack('s', fft_input)[0]

            #indice = getIndice(fft_input)
            #valReelle = getReelle(fft_input)
            #valIm = getIm(fft_input)

            #print "indice = " + str(indice)
            #print "valReelle = " + str(valReelle)
            #print "valIm = " + str(valIm)

            print fft_input

            # Les coefficients reels sont sur les indices pairs
            # Les coefficients imaginaires sont sur les indices impairs
            # fft[indice] = valReelle
            # fft[indice + 1] = valIm

finally:
    p.disconnect()
