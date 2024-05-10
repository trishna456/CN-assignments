import socket
import threading
import os
def chat_server(iface:str, port:int, use_udp:bool) -> None:
    addrInfo = socket.getaddrinfo(iface, port);
    #print(addrInfo)
    if(use_udp):
        #print("This is a UDP call");
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #s.bind(('',port))
        s.bind(addrInfo[0][4])
        print("Hello, I am a server");
        while(True):
            recvData,addr = s.recvfrom(port)
            while(recvData):
                strData = recvData.decode().strip();
                if(len(strData)>=256):
                    strData = strData[0:255]
                print("got message from",addr)
                if(strData == "hello"):
                    s.sendto("world\n".encode(),addr);
                elif(strData == "goodbye"):
                    s.sendto("farewell\n".encode(),addr)
                    break;
                elif(strData == "exit"):
                    s.sendto("ok\n".encode(),addr)
                    return
                else:
                    s.sendto(strData.encode(),addr);
                break

    else:
        #print("This is a TCP call");
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.bind(('',port))
        s.bind(addrInfo[0][4])
        s.listen()
        print("Hello, I am a server");
        num = 0
        while(True):
            c,addr = s.accept()
            print("connection",num,"from",addr);
            num += 1
            thread = threading.Thread(target = connect_client, args = (c,addr,num))
            thread.start()

def connect_client(c,addr,num):
    while(c):
        #print("connection",num,"from",addr);
        while(True):
            data = c.recv(256)
            if not data:
                break
            strData = data.decode().strip();
            if(len(strData)>=256):
                strData = strData[0:255]
            print("got message from",addr);
            if(strData == "hello"):
                c.send("world\n".encode());
            elif(strData == "goodbye"):
                c.send("farewell\n".encode());
                c.close();
                break;
            elif(strData == "exit"):
                c.send("ok\n".encode());
                c.close()
                os._exit(0)
            else:
                c.send(strData.encode());
        break


def chat_client(host:str, port:int, use_udp:bool) -> None:
    if(use_udp):
        #print("This is a UDP call");
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addrInfo = socket.getaddrinfo(host, port, family=socket.AF_INET, proto=socket.IPPROTO_UDP)
    else:
        #print("This is a TCP call");
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addrInfo = socket.getaddrinfo(host, port, family=socket.AF_INET, proto=socket.IPPROTO_TCP)
    finalAddrInfo = addrInfo[0][4]
    print("Hello, I am a client");
    s.connect(finalAddrInfo)
    while(True):
        sendData = input()
        if(len(sendData)>=256):
            sendData = sendData[0:255]
        s.send(sendData.encode())
        data = s.recv(256).decode().strip();
        print(data)
        if((data == "ok" and sendData == "exit") or (data == "farewell" and sendData == "goodbye")):
            s.close();
            break;
