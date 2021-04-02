
def sendMessage(socket, message):
    msglen = str(len(message))
    msg = msglen.encode()+b":"+ message # add msg length to message
    while len(msg): # send until message done
        bytes = socket.send(msg)
        msg = msg[bytes:]

buffer = ""
        
def receiveMessage(socket):
    global buffer
    if(buffer == ""):
        buffer += socket.recv(100).decode()
    lenMsg = ""

    for i in range(len(buffer)): # split the buffer and length
        if buffer[i] == ":":
            buffer = buffer[i+1:]
            break
        lenMsg += buffer[i]

    if(lenMsg == ""): # if no length then return nothing
        return ""

    intlenMsg = int(lenMsg) # change data type to int for message length
    msg = ""
    
    while((len(msg) < intlenMsg)): # add buffer message into actual msg to receive
        if(len(buffer) == 0):
            bufer = socket.recv(100).decode()
        msg += buffer[0]
        buffer = buffer[1:]
    return msg
