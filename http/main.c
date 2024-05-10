#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

void send_http(char* host, char* msg, char* resp, size_t len);


/*
  Implement a program that takes a host, verb, and path and
  prints the contents of the response from the request
  represented by that request.
 */
 
 /*
  sample input
  www.example.com GET /
 */
 
int main(int argc, char* argv[]) {

  if(argc != 4) {
    printf("Invalid arguments - %s <host> <GET|POST> <path>\n", argv[0]);
    return -1;
  }
  
  char* host = argv[1];
  char* verb = argv[2];
  char* path = argv[3];
  char resp[1024000]="";

  /* Adding a Host:<host> header */
  int  headerLen = strlen("Host:")+strlen(host);
  // printf("%u",headerLen);

  char* header = (char*)malloc(headerLen*sizeof(char));
  strcat(header,"Host:");
  strcat(header,host);
  // printf("%s",header);
  /* End of Adding a  Host:<host> header */

  /* Creating HTTP request message */
  char* httpReq = (char*)malloc(3000);
  strcat(httpReq,verb);
  strcat(httpReq," ");
  strcat(httpReq,path);
  strcat(httpReq," ");
  strcat(httpReq,"HTTP/1.0\r\n");
  strcat(httpReq, header);
  strcat(httpReq,"\r\n");
  /* End of Creating HTTP request message */

  /* Updating value for GET request */
  if(strcmp(verb,"GET")==0){
    strcat(httpReq,"\r\n");
  }
  /* End of Updating value for GET request */

  /* Updating value for POST request */
  else if(strcmp(verb,"POST")==0){
    strcat(httpReq,"Content-Length:17\r\n\r\n");
    strcat(httpReq,"Post Hello World\r\n\r\n");
  }
  /* End of Updating value for POST request */

  // printf("%s",httpReq);

  /* Making HTTP call */
  send_http(host,httpReq,resp,4096);
  /* End of Making HTTP call */

  printf("%s",resp);

  return 0;
}
