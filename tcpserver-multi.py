"""
Server side: open a socket on a port, listen for a message 
from a client, and send an echo reply; 
echoes lines until eof when client closes socket; spawns a 
thread to handle each client connection; threads share global 
memory space with main thread.
"""

from socket import *
import _thread as thread
import time

def now():
    """
    returns time of day
    """
    return time.ctime(time.time())


def handleClient(connection):
    """
    a client handler function
    """

    while True:
        data = connection.recv(1024).decode()
        print("Recieved message = ", data)
        modified_message = data.upper()
        connection.send(modified_message.encode())
        if(data == "exit"):
            break
    connection.close()

def main():
    """
    creates a server socket, listens for new connections,
    and spawns a new thread whenever a new connection joins
    """
    serverPort = 12222
    serverName = '172.20.35.32' #10.47.15.70
    serverSocket = socket(AF_INET, SOCK_STREAM)

    try:
        serverSocket.bind((serverName,serverPort))
    except:
        print("Bind failed. Error: ")

    serverSocket.listen(1)
    print("The server is ready to recieve")
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Server connected by ", addr)
        print(" at ", now())
        thread.start_new_thread(handleClient, (connectionSocket,))

    serverSocket.close()

if __name__ == '__main__':
    main()
