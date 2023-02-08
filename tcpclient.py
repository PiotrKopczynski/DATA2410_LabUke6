from socket import *
serverName = '172.20.35.32'
serverPort = 12222
clientSocket = socket(AF_INET,SOCK_STREAM) 
clientSocket.connect((serverName,serverPort))
sentence = input("Input lowercase sentence:")
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print("From Server: ", modifiedSentence.decode())
clientSocket.close()