#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>
#include <netdb.h>
#include <math.h>
#include <arpa/inet.h>

/*
  Use the `getaddrinfo` and `inet_ntop` functions to convert a string host and
  integer port into a string dotted ip address and port.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }

  char* host = argv[1];
  long port = atoi(argv[2]);

  /*  Creating hints argument */
  struct addrinfo hints;
  memset(&hints,0,sizeof(hints));
  hints.ai_flags = AI_PASSIVE; //wildcard IP addresses
  hints.ai_family = PF_UNSPEC; //to allow both IPv4 and IPv6 addresses
  hints.ai_protocol = IPPROTO_TCP; 
  hints.ai_socktype = SOCK_STREAM;
  /* End of creating hints argument */;

  /* Finding number of characters in 'port' to allocate memory appropriately */
  long num = port;
  int portLen = 0;
  while(num>0){
	  portLen++;
	  num/=10;
  }
  // printf("\n Total numbers of characters in port are %d",portLen);
  /* End of finfing number of characters in 'port' */

  /* Converting port number to char pointer before passing it to getaddrinfo */
  char* sport = malloc((sizeof(char) * portLen) + 1);
  sprintf(sport,"%ld",port);
  // printf("\nchar port number is %s",sport);
  /* End of converting port number to char pointer */
  
  /* Creating variables to store result, calling getaddrinfo, handling error */
  struct addrinfo *resultList;
  struct addrinfo *nextResult;
  int errorNo = 0; //in case the function returns any error
  errorNo = getaddrinfo(host, sport, &hints, &resultList);
  if(errorNo){
	  printf("\n Error while calling the function %s", gai_strerror(errorNo)); //displaying errors if any, in readable format
	  return 0;
  }
  /* End of calling getaddrinfo, handling error */
  
  /* Looping through the result list */
  nextResult = resultList;
  char* finalIP = malloc(4096);
  while(nextResult!=NULL){
	  // A few parts from the below code snippet are adapted from the manual pages of getaddrinfo and inet_ntop
	  void* raw_address;
	  if(nextResult->ai_family == AF_INET){
		 // printf("\nThis is an IPv4 address");
		  struct sockaddr_in* temp = (struct sockaddr_in*)nextResult->ai_addr; //cast address into AF_INET container
		  raw_address = &(temp->sin_addr); //Extract address from the container
	         // printf("\nThe raw address is %p",raw_address);
		  inet_ntop(AF_INET,raw_address,finalIP,4096);
		  printf("\nIPv4 %s",finalIP);
	  }
	  else if(nextResult->ai_family == AF_INET6){
		 // printf("\nThis is an IPv6 address");
		  struct sockaddr_in6* temp = (struct sockaddr_in6*)nextResult->ai_addr; //cast address into AF_INET6 container
                  raw_address = &(temp->sin6_addr); //Extract address from the container
		 // printf("\nThis raw address is %p",raw_address);
                  inet_ntop(AF_INET6,raw_address,finalIP,4096);
                  printf("\nIPv6 %s",finalIP);
	  }
	  nextResult = nextResult->ai_next;
  }

  return 0;

}
