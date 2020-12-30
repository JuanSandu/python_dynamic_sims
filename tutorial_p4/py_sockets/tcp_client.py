import socket
import sys

# Basic configuration
msg = "Hey there"
PORT = 3333
buffer_size = 1024
family_addr = socket.AF_INET  # IP4 here. For IP6 use: socket.AF_INET6
host = '0.0.0.0'  # For IP6, change the address.

sock = socket.socket(family_addr, socket.SOCK_STREAM)  # Create the socket
sock.connect((host, PORT))  # Connect it

while True:
    sock.sendall(msg)  # Send a message and the server should answer to it
    data = sock.recv(buffer_size)  # Wait here for a message
    print("Received: {}".format(data))

sock.close()  # Close at the end
