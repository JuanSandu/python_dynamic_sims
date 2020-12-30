import socket
import sys

# Basic configuration
msg = "Hey there"
PORT = 3333
buffer_size = 512

host = '0.0.0.0'  # For IP6, change the address.
family_addr = socket.AF_INET
sock = socket.socket(family_addr, socket.SOCK_DGRAM)

while True:
    sock.sendto(msg, (host, PORT))
    reply, addr = sock.recvfrom(buffer_size)  # Receive data from the socket
    print('Reply from server: '  + str(reply))
