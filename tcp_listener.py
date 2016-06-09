import socket
import sys
import threading
import signal
from subprocess import call

import time


class Listener:
    my_connection = None
    connections = []

    def __init__(self,cmd_handler):
        self.availableData = ""
        self.hasCommand = False
        self.cmd_handler = cmd_handler

    def openHabListener(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('localhost', 5005)
        print >>sys.stderr, 'tcp connection up on %s port %s' % server_address
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)

        while True:
            # Wait for a connection
            print >>sys.stderr, 'waiting for a tcp connection'
            connection, client_address = sock.accept()
            Listener.my_connection = connection
            Listener.connections.append(connection)
            try:
                print >>sys.stderr, 'tcp connection from', client_address

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    print >>sys.stderr, 'tcp received "%s"' % data
                    self.availableData += data

                    if data:
                        print >>sys.stderr, 'tcp sending data back to the client'
                        self.cmd_handler(data)
                        connection.sendall(data)
                    else:
                        print >>sys.stderr, 'tcp no more data from', client_address
                        self.cmd_handler(data)
                        break

            finally:
                # Clean up the connection
                connection.close()

    def start_listening(self):
        self.t = threading.Thread(target=self.openHabListener)
        self.t.daemon=True
        self.t.start()

time.sleep(5)
