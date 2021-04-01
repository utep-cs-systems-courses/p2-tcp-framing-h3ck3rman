#! /usr/bin/env python3

import socket, sys, re, time, os
sys.path.append("../lib")       # for params
import params
import framedSocket

progname = "fileClient"

try:                            # tries to get the necessary parameters
    clientFile = sys.argv[1]        
    serverHost, serverFile = re.split(":", sys.argv[2])
    serverPort = 50001
except:                         # if it fails, prints syntax.
    print("Bad param format: '%s'. Should be $ ./fileClient Send {clientFile} {host:serverFile}\n" % sys.argv)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d\n" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s\n" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s\n" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s\n" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket\n')
    sys.exit(1)

framedSocket.sendMessage(s,sys.argv[0].encode())  # sent the mode, "Send", "Recv" later if needed
framedSocket.sendMessage(s,serverFile.encode())   # sent the file name to be saved on server side
response = framedSocket.receiveMessage(s)         # gets response from the server, "OK" or "NO"
if(response == "OK"):
    fd = os.open("./client/"+clientFile, os.O_RDONLY)
    next = 0
    limit = 0
    sbuf = ""
    ibut = ""
    message= ""
    while 1:
        ibuf = os.read(fd, 100)
        sbuf = ibuf.decode()
        limit = len(sbuf)
        if limit == 0:
            break
        message += sbuf 
    framedSocket.sendMessage(s, message.encode())   # sends it to the server in the framed send
    result = framedSocket.receiveMessage(s)                 # recieves a result of the transfer
    print(result+"\n")                    # prints result, "SUCCESS" or "FAILURE WRITING FILE"
else: 
    print("File name already taken on server file\n")  # response was "NO"
s.close()
