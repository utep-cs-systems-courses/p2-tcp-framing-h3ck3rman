
def sendMessage(socket, message):
    msglen = str(len(message))
    #add msg length to message
    msg = msglen.encode()+b":"+ message
    #send until message done
    while len(msg):
        bytes = socket.send(msg)
        msg = msg[bytes:]

buffer = ""
        
def recieveMessage(socket):
    global buffer
    buffer += socket.recv(100).decode()
    lenMsg = ""

    #split the buffer and length of message
    for i in range(len(buffer)):
        if buffer[i] == ":":
            buffer = buffer[i+1:]
            break
        lenMsg += buffer[i]

    #if no length then return nothing
    if(lenMsg == ""):
        return ""

    #change data type to int for message length
    intlenMsg = int(lenMsg)
    
    msg = ""
    #add buffer message into actual msg to receive
    while((len(msg) < intlenMsg)):
        msg += buffer[0]
        if(len(buffer) == 1):
            buffer = socket.recv(100).decode()
        buffer = buffer[1:]
    return msg
