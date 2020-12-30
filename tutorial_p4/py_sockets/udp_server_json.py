import socket
import sys
import time
import json   # <----

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
    data_dict = json.loads(data)  # <----
    print('Received: {} with floating number: {}'.format(data, data_dict["Acc_x"]))  # <----
    reply = 'Thanks'
    sock.sendto(reply, addr)
    time.sleep(1.5)

sock.close()
