from socket import  *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

message = raw_input("input message:")

clientSocket.sendto(message, (serverName, serverPort))
modifyMessage, serverAddress = clientSocket.recvfrom(2048)

print(modifyMessage)
clientSocket.close()