from socket import *
import sys
import threading

serverName = gethostbyname(gethostname()) # This function automatically fetches the local IP
port = 12220
addr = (serverName, port)

nickname = input('Choose a nickname >>>') # The user inputs a nickname that will be used by the server
client = socket(AF_INET,SOCK_STREAM)

try:
    client.connect((serverName,port))
except:
    print("ConnectionError")
    sys.exit()

def recieveBroadcast():
    """
    Function: A function for recieving messages from the server.
    Exceptions: If the function fails to recieve a message from the server,
    the client socket is closed and the while loop is stopped.
    """
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "Nickname:":
                client.send(nickname.encode())
            else:
                print(message)
        except:
            client.close()
            break

def clientSend():
    """
    Function: A function for sending messages to the server.
    """
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

