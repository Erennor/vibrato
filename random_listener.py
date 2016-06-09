import socket
import sys
import threading
import uinput
import time

device = uinput.Device([
	uinput.KEY_LEFT,
	uinput.KEY_RIGHT
	])

class RandomListener:
    my_connection = None
    connections = []

    def __init__(self):
        self.availableData = ""
        self.hasCommand = False

    def openHabListener(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('localhost', 5006)
        print >>sys.stderr, 'tcp connection up on %s port %s' % server_address
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)

        while True:
            # Wait for a connection
            print >>sys.stderr, 'waiting for a tcp connection'
            connection, client_address = sock.accept()
            RandomListener.my_connection = connection
            RandomListener.connections.append(connection)
            try:
                print >>sys.stderr, 'tcp connection from', client_address

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    print >>sys.stderr, 'tcp received "%s"' % data
                    self.availableData += data
                    device.emit_click(uinput.KEY_RIGHT)

                    if data:
                        print >>sys.stderr, 'tcp sending data back to the client'
                        connection.sendall(data)
                    else:
                        print >>sys.stderr, 'tcp no more data from', client_address
                        break

            finally:
                # Clean up the connection
                connection.close()

    def start_listening(self):
        self.t = threading.Thread(target=self.openHabListener)
        self.t.daemon=True
        self.t.start()

if __name__ =="__main__":
    random_listener = RandomListener()
    random_listener.start_listening()
    while True:
        time.sleep(1)
