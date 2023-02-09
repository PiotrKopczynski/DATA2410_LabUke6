from socket import *
import sys

serverName = '172.20.35.32' #10.47.15.70
serverPort = 12222

clientSocket = socket(AF_INET,SOCK_STREAM)
try:
    clientSocket.connect((serverName,serverPort))
except:
    print("ConnectionError")
    sys.exit()

while True:
    sentence = input("Input lower case sentence: ")
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024).decode()
    print("From server: ", modifiedSentence)
    if (sentence == "exit"):
        break

clientSocket.close()