// Server side C/C++ program to demonstrate Socket programming
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include "frozen.c"
#define PORT 3333

char *hello = "Hello from server";
char *ok_msg = "OK";
char json_buffer[256] = {0};


void data_to_json(char *char_buffer, float *imu_data){
  struct json_out out_buffer = JSON_OUT_BUF(char_buffer, 1024);
  json_printf(&out_buffer, "{AcX: %f}", imu_data[0]);
}


int create_socket_and_connect(struct sockaddr_in *serv_addr, int *server_fd){
  int addrlen = sizeof(*serv_addr);
  int sock, opt=1;
  // Creating socket file descriptor
  // SOCK_STREAM = TCP
  // SOCK_DGRAM = UDP
  if ((*server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0){
      perror("Error: socket creating function failed.");
      exit(EXIT_FAILURE);
  }

  if (setsockopt(*server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
                                                &opt, sizeof(opt))){
      perror("Error: setsockopt function failed.");
      exit(EXIT_FAILURE);
  }
  serv_addr->sin_family = AF_INET; // IPv4
  serv_addr->sin_addr.s_addr = INADDR_ANY; // INADDR_ANY = Localhost, otherwise, IP serv_addr
  serv_addr->sin_port = htons( PORT );

  // Forcefully attaching socket to the port 8080
  if (bind(*server_fd, (struct sockaddr *)serv_addr, sizeof(*serv_addr))<0){
      perror("Error: Bind function failed.");
      exit(EXIT_FAILURE);
  }
  if (listen(*server_fd, 3) < 0){
      perror("Error: Listenning function failed.");
      exit(EXIT_FAILURE);
  }

  printf("Accepting connections..\n");
  // Next function ( accept() ) is blocking until a connection request is given
  if ((sock = accept(*server_fd, (struct sockaddr *)serv_addr, (socklen_t*)&addrlen))<0){
      perror("Error: Accepting process failed.");
      exit(EXIT_FAILURE);
  }

  return sock;
}


int main(int argc, char const *argv[])
{
    int server_fd, sock, valread;
    struct sockaddr_in serv_addr;
    char buffer[10] = {0};
    float imu_data[3] = {0.0};

    sock = create_socket_and_connect(&serv_addr, &server_fd);
    printf("Socket created.\n");

    while (1){
      valread = recv(sock, buffer, 10, MSG_WAITALL);
      printf("Client message: %s\n", buffer);
      memset(buffer, 0, 10);

      imu_data[0] = 1.234;
      data_to_json(json_buffer, imu_data);
      send(sock, json_buffer, strlen(json_buffer), 0);
      printf("OK message sent.\n");
    }
    // Close the socket
    close(server_fd);

    return 0;
}
