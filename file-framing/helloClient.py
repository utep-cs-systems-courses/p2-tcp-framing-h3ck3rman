#! /usr/bin/env python3

# Echo client program
import socket, sys, re, time, os
sys.path.append("../lib")       # for params
import params
import framedSocket

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

delay = float(paramMap['delay']) # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(delay)
    print("done sleeping")


framedSocket.sendMessage(s, b"Send")
framedSocket.sendMessage(s, b"text.txt")
fd = os.open("./client/text.txt", os.O_RDONLY)
next = 0
limit = 0
sbuf = ""
ibuf = ""
message = ""
while 1:
    ibuf = os.read(fd, 100)
    sbuf = ibuf.decode()
    limit = len(sbuf)
    if limit == 0:
        break
    message += sbuf
framedSocket.sendMessage(s, message.encode())
s.close()
