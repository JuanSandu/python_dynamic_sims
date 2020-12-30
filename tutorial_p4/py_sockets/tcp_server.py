import socket
import sys
import time

# Basic configuration
PORT = 3333
buffer_size = 128
family_addr = socket.AF_INET  # For IPv6: socket.AF_INET6

sock = socket.socket(family_addr, socket.SOCK_STREAM)
sock.bind(('', PORT))  # Bind the socket to the local address

sock.listen(2)  # Enable the socket to accept connections

conn, addr = sock.accept()  # Wait for a connection
print('Connected with: {}'.format(addr))

while True:
    data = conn.recv(buffer_size)  # Receive data from client.
    print('Received data: {}'.format(data))
    reply = 'We received your message: ' + data
    conn.send(reply)  # Send an answer
    time.sleep(1.5)
conn.close()
