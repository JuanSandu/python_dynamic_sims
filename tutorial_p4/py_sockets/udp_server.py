import socket
import sys
import time

# Basic configuration
IP_VERSION = 'IPv4'
PORT = 3333
buffer_size = 1024

family_addr = socket.AF_INET

sock = socket.socket(family_addr, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))

while True:
    print('Waiting for data...')
    data, addr = sock.recvfrom(buffer_size)
    print('Received: ' + data)
    reply = 'Thanks'
    sock.sendto(reply, addr)
    time.sleep(1.5)

sock.close()
