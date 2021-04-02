#! /usr/bin/env python3

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
import framedSocket

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileServer"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

while True:
    conn, addr = s.accept() # wait until incoming connection request
    if os.fork() == 0:      # child becomes server
        print("Connected by: %s %d\n"%addr)  # prints where connection comes from
        framedSocket.receiveMessage(conn)    # receives "Send"
        filename = framedSocket.receiveMessage(conn)  # receives the name of the file to save
        if os.path.isfile("./server/"+filename): # checks if file already exists
            framedSocket.sendMessage(conn,b"NO")
        else:
            framedSocket.sendMessage(conn,b"OK")
            try:                                    # tries to write to the file
                fd = os.open("./server/"+filename, os.O_CREAT | os.O_WRONLY)
                os.write(fd, framedSocket.receiveMessage(conn).encode())
                os.close(fd)
                framedSocket.sendMessage(conn,b"SUCCESS")          # success
            except:
                framedSocket.sendMessage(conn,b"FAILURE WRITING FILE")
        conn.shutdown(socket.SHUT_WR)


