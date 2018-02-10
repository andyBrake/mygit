from socket import  *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("the server is ready to recv:")

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print("from %s recv %s"%(clientAddress, message))
    modifyMessage = message.upper()
    serverSocket.sendto(modifyMessage, clientAddress)