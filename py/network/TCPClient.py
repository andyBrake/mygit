from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

message = raw_input("input:")
clientSocket.send(message)

modifyMessage = clientSocket.recv(1024)
print("recv message: %s"%modifyMessage)
clientSocket.close()
