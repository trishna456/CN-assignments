from typing import BinaryIO
import socket

def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    addrInfo = socket.getaddrinfo(iface, port);
    if(use_udp):
        #print("This is a UDP call");
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if(iface is None):
            s.bind(('',port))
        else:
            s.bind(addrInfo[0][4])
        print("Hello, I am a server");
        while(True):
            recvData,addr = s.recvfrom(port)
            fp.write(recvData);
            if(len(recvData)==0):
                s.close()
                break

    else:
        #print("This is a TCP call");
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(iface is None):
            s.bind(('',port))
        else:
            s.bind(addrInfo[0][4])
        s.listen()
        print("Hello, I am a server");
        c,addr = s.accept()
        while(True):
            data = c.recv(256)
            fp.write(data);
            if(len(data)==0):
                s.close()
                break;

def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    if(use_udp):
        #print("This is a UDP call");
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addrInfo = socket.getaddrinfo(host, port, family=socket.AF_INET, proto=socket.IPPROTO_UDP)
    else:
        #print("This is a TCP call");
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addrInfo = socket.getaddrinfo(host, port, family=socket.AF_INET, proto=socket.IPPROTO_TCP)
    finalAddrInfo = addrInfo[0][4]
    if(finalAddrInfo is None):
        s.connect(('',port));
    else:
        s.connect(finalAddrInfo)
    print("Hello, I am a client");
    sendData = fp.read()
    i = 0;
    while(i<=len(sendData)):
        sendBits = sendData[i:i+256]
        s.send(sendBits)
        i+=256
    s.send("".encode());
    s.close();
