import socket
import sys
import json  # <----

# Basic configuration
msg_dict = {"Acc_x": 0.0}  # <----
PORT = 3333
buffer_size = 512

host = '0.0.0.0'  # For IP6, change the address.
family_addr = socket.AF_INET
sock = socket.socket(family_addr, socket.SOCK_DGRAM)

while True:
    msg_dict["Acc_x"] = 1.3211  # <----
    sock.sendto(json.dumps(msg_dict), (host, PORT))  # <----
    reply, addr = sock.recvfrom(buffer_size)  # Receive data from the socket
    print('Reply from server: '  + str(reply))
