// Client side C/C++ program to demonstrate Socket programming

#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#define PORT 3333

char *msg = "Hi there!\r";


void delay_ms(int msec){
  // This function has been adapted from:
  // https://www.geeksforgeeks.org/time-delay-c/
  // Converting time into micro_seconds
  int usec = 1000 * msec;
  // Storing start time
  clock_t start_time = clock();
  // looping till required time is not achieved
  while (clock() < start_time + usec){};
}


int create_socket_and_connect(struct sockaddr_in *serv_addr){
  int sock, opt=1;
  // Create the socket
  // AF_INET = IPv4
  // AF_INET6 = IPv6
  if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0){
      printf("\nError: Socket creation error \n");
      return -1;
  }

  // Set wait timeout
  struct timeval tv;
  tv.tv_sec = 0;
  tv.tv_usec = 300;
  setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof tv);

  serv_addr->sin_family = AF_INET;
  serv_addr->sin_port = htons(PORT);
  // Convert IPv4 and IPv6 addresses from text to binary form
  if(inet_pton(AF_INET, "0.0.0.0", &(serv_addr->sin_addr))<=0){
      printf("\nError: Invalid address / Address not supported \n");
      return -1;
  }
  printf("Attempting to connect..\n");
  if (connect(sock, (struct sockaddr *)serv_addr, sizeof(*serv_addr)) < 0){
      printf("\nError: Connection Failed \n");
      return -1;
  }

  return sock;
}


int main(int argc, char const *argv[]){
  struct sockaddr_in serv_addr;
  char buffer[1024] = {0};
  int sock = 0, ret;

  sock = create_socket_and_connect(&serv_addr);
  printf("Socket created.\n");

  while (1){
    send(sock, msg, strlen(msg), 0);
    printf("Message sent.\n");

    ret = recv(sock, buffer, 1024, MSG_WAITALL);
    printf("Server answer: %s\n", buffer);

    // Add some delay here
    delay_ms(500);
  }
  close(sock);
  return 0;
}
