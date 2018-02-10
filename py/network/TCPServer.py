from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("server is ready to recv:")

while True:
    connectSocket, addr = serverSocket.accept()
    message = connectSocket.recv(1024)
    connectSocket.send(message.upper())
    connectSocket.close()