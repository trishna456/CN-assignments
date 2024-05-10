# reference -  https://www.baeldung.com/cs/networking-go-back-n-protocol

from typing import BinaryIO
import socket
import pickle
import time
import math

def gbn_server(iface:str, port:int, fp:BinaryIO) -> None:
    addrInfo = socket.getaddrinfo(iface,port,family=socket.AF_INET)[0]
    #print("addrInfo", addrInfo)
    args = (addrInfo[4][0], port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(args)
    s.settimeout(0.05)
    print("Hello, I am a server");
    EOF = 0
    currData = []
    counter = 0
    receiveTime = time.time()
    while True:
        try:
            data, addr = s.recvfrom(1024)
            current = []
            current = pickle.loads(data)
            #print("current", current)
            if(current!=None):
                s.settimeout(0.05)
                #print("setting timeout")
            if(current[1]==counter):
                if(current[2]):
                    currData.append(current[2])
                else:
                    EOF = 1
                counter+=1
                currentAck = 2
            else:
                currentAck = 1
            #print("final ack", currentAck)
            #print("file end reached", EOF)
            #print("currData", currData)
            #print("counter", counter)
            nextPkt = []
            nextPkt.append(currentAck)
            nextPkt.append(counter)
            #print("next packet", nextPkt)
            s.sendto(pickle.dumps(nextPkt),addr)
        except:
            if(EOF==1):
                currentTime = time.time()
                if((currentTime-receiveTime)>0.3):
                    break
    for data in currData:
        fp.write(data)
    fp.close()
    s.close()

def gbn_client(host:str, port:int, fp:BinaryIO) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addrInfo = socket.getaddrinfo(host,port,family=socket.AF_INET)[0]
    args = (addrInfo[4][0], port)
    #print("args", args)
    print('Hello I am a client')
    counter = 0
    slidingWindow = []
    windowSize = 4
    bs = 1
    currentAck = 2
    ackTime = time.time()
    fileData = fp.read(256)
    EOF = 0
    while((not EOF) or (len(slidingWindow)!=0)):
        totalSize = bs+windowSize
        #print("totalSize", totalSize)
        #print("counter", counter)
        #print("file end", EOF)
        if((counter<totalSize) and (not EOF)):
            if(not fileData):
                EOF = 1
            nextPkt = []
            nextPkt.append(currentAck)
            nextPkt.append(counter)
            nextPkt.append(fileData)
            #print("next packet", nextPkt)
            s.sendto(pickle.dumps(nextPkt,protocol=pickle.DEFAULT_PROTOCOL),args)
            counter+=1
            slidingWindow.append(nextPkt)
            fileData = fp.read(256)
            s.settimeout(0.05)
            #print("final window", slidingWindow)
        try:
            data, addr = s.recvfrom(1024)
            s.settimeout(0.05)
            receivedPkt = []
            receivedPkt = pickle.loads(data)
            #print("received packet", receivedPkt)
            if(receivedPkt[0]==2):
                if(receivedPkt[1]==bs):
                    ackTime = time.time()
                    del slidingWindow[0]
                    bs+=1
            else:
                time.sleep(0.05)

        except socket.timeout:
            currentTime = time.time()
            if((currentTime-ackTime) > 0.3):
                for i in slidingWindow:
                    s.sendto(pickle.dumps(i),args)
    s.close()
