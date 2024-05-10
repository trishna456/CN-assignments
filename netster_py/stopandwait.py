from typing import BinaryIO
import socket

def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    if(iface is None):
        iface = ""
    args = (iface,port)
    # sockets reference link - https://docs.python.org/3/library/socket.html#
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(args)
    print("Hello, I am a server")
    fileData = bytes()
    flagBit = 1
    while True:
        try:
            dataaddr = s.recvfrom(256)
            #print("\r",dataaddr)
            if(dataaddr!=-1):
                if(dataaddr[0]!=b''):
                    if(flagBit==1):
                        flagBit = 0
                        fileData+=dataaddr[0]
                        s.sendto('1'.encode(),dataaddr[1])
                    else:
                        flagBit = 1
                        fileData+=dataaddr[0]
                        s.sendto('0'.encode(),dataaddr[1])
                else:
                    fp.write(fileData)
                    s.close()
                    exit(1)
            else:
                continue

        except Exception as err:
            print('Error!',err)

        except socket.timeout:
            continue

def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
    print("Hello, I am a client")
    args = (host,port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(args)
    s.settimeout(3)
    whileFlag = False
    try:
        flagBit = 0
        while True:
            fileData = fp.read(256)
            while True:
                if(fileData!=b''):
                    try:
                        s.sendto(fileData,args)
                        s.settimeout(3)
                        dataaddr = s.recvfrom(256)
                        if(flagBit==0):
                            if(dataaddr[0].decode().strip()=="0"):
                                continue
                            elif(dataaddr[0].decode().strip()=="1"):
                                flagBit = 1
                                break
                        elif(flagBit==1):
                            if(dataaddr[0].decode().strip()=="1"):
                                continue
                            elif(dataaddr[0].decode().strip()=="0"):
                                flagBit = 0
                                break
                    except socket.timeout:
                        continue
                else:
                    whileFlag = True
                    break
            if whileFlag:
                break

        s.sendto(''.encode(),args)
        s.close()
        exit(1)

    except Exception as err:
        print('Error!',err)
        exit(1)
