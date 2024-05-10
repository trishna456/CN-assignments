#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int connect_smtp(const char* host, int port);
void send_smtp(int sock, const char* msg, char* resp, size_t len);



/*
  Use the provided 'connect_smtp' and 'send_smtp' functions
  to connect to the "lunar.open.sice.indian.edu" smtp relay
  and send the commands to write emails as described in the
  assignment wiki.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }

  char* rcpt = argv[1];
  char* filepath = argv[2];
  char response[4096];
  int socket = connect_smtp("lunar.open.sice.indiana.edu", 25);
  // printf("%d", socket);  

  /** 
  * The below code snippet to read a file was adapted from dmityugov's comment on "How to read the content of a file to a string in C?"
  * link here:
  * https://stackoverflow.com/questions/174531/how-to-read-the-content-of-a-file-to-a-string-in-c
  */
  
  // start snippet -> code to read a file	
  FILE* ptr;
  ptr=fopen(filepath,"r");
  char* buffer = NULL;
  size_t len;
  ssize_t bytes_read =  getdelim( &buffer, &len, '\0', ptr);
  if ( bytes_read != -1) {
	//printf("%s",buffer);
  }
  // end snippet -> code to read a file
	
  // adding . at the end of the message
  char* msg = (char*)malloc(10000);
  strcat(msg, buffer);
  strcat(msg,"\n.\r\n");
 //  printf("message data is");
 //  printf("%s",msg);

  char* mailFrom = (char*)malloc(10000);
  strcat(mailFrom, "MAIL FROM: <");
  strcat(mailFrom,  rcpt);
  strcat(mailFrom, ">\r\n");
 //  printf("%s", mailFrom);

  char* mailTo = (char*)malloc(10000);
  strcat(mailTo, "RCPT TO: <");
  strcat(mailTo,  rcpt);
  strcat(mailTo, ">\r\n");
 //  printf("%s", mailTo);

  send_smtp(socket,"HELO iu.edu\r\n", response, 4096);
  printf("%s\n", response);
  send_smtp(socket,mailFrom, response, 4096);
  printf("%s\n", response);
  send_smtp(socket,mailTo, response, 4096);
  printf("%s\n", response);
  send_smtp(socket,"DATA\r\n", response, 4096);
  printf("%s\n", response);
  send_smtp(socket,msg,response, 4096);
  printf("%s", response);
  send_smtp(socket,"QUIT\r\n", response, 4096);
 // printf("%s\n", response);

  return 0;
}
