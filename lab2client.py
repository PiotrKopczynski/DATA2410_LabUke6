from socket import *
import sys
import threading

serverName = gethostbyname(gethostname())
port = 12222
addr = (serverName, port)

#alias = input('Choose an alias >>>')
client = socket(AF_INET,SOCK_STREAM)
try:
    client.connect((serverName,port))
except:
    print("ConnectionError")
    sys.exit()

def recieveBroadcast():
    while True:
        try:
            message = client.recv(1024).decode()
            print("\nMessage from server: ", message)
        except:
            print("Broadcast error!")
            client.close()
            break

def clientSend():
    while True:
        message = input("Input:")
        client.send(message.encode())
        if message=="exit":
            break
    client.close()



broadcast_thread = threading.Thread(target=recieveBroadcast)
broadcast_thread.start()

sending_thread = threading.Thread(target=clientSend)
sending_thread.start()

