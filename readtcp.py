#!/usr/bin/env python

import socket


TCP_IP = 'nodemcu-1'
TCP_PORT = 21
BUFFER_SIZE = 10
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
#s.send(MESSAGE)
for i in range(1, 1000):
    data = s.recv(BUFFER_SIZE)
    print "received data:", data
s.close()

#print "received data:", data