from socket import *

serverPort = 12222
serverName = '172.20.35.32'

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName,serverPort))
print("The server is ready to recieve! :)")

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)