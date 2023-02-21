from socket import *
import sys
import threading
import time

serverName = gethostbyname(gethostname())
port = 12222
addr = (serverName, port)

nickname = input('Choose a nickname >>>')
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
            if message == "Nickname:":
                client.send(nickname.encode())
            else:
                print(message)
        except:
            #print("Broadcast error!")
            client.close()
            break

def clientSend():
    while True:
        #message = f'{nickname}: {input("")}'
        message = input("")
        client.send(message.encode())
        if message == "exit":
            print("You have exited the server.")
            break
    client.close()



broadcast_thread = threading.Thread(target=recieveBroadcast)
broadcast_thread.start()

sending_thread = threading.Thread(target=clientSend)
sending_thread.start()

