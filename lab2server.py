from socket import * 
import threading
import _thread as thread
import time

clients = []
newClientMessage = "A new user just joined the server! :O\n"
#aliases = []

def now():
    """
    returns time of day
    """
    return time.ctime(time.time())

def broadcast(message):
    for client in clients:
        client.send(message.encode())

def game(players):
    #to be implemented
    for player in players:
        print("hei")


def handleClient(client, addr):
    """
    a client handler function
    """

    while True:
        try:
            message = client.recv(1024).decode()
            print(addr,"Recieved message: ",message)
            if message=="exit":
                clients.remove(client)
                client.close()
                break
            else:
                client.send("Message was recieved!".encode())
        except:
            #index = clients.index(client)
            clients.remove(client)
            client.close()
            #alias = aliases[index]
            broadcast("A user has left the server ;(.")
            #aliases.remove(alias)
            break





def main():

    serverPort = 12222
    serverName = gethostbyname(gethostname())
    serverSocket = socket(AF_INET, SOCK_STREAM)

    try:
        serverSocket.bind((serverName,serverPort))
    except:
        print("Bind failed. Error: ")
    
    serverSocket.listen(1)
    print("The server is open! :D")

    while True:
        newClient, addr = serverSocket.accept()
        newClient.send("You are now connected! :O".encode())
        print("SERVER CONNECTED TO BY ", addr)
        print(" AT ", now())
        broadcast(newClientMessage)
        clients.append(newClient)
        print("AMOUNT OF CURRENT USERS: ",len(clients))

        client_thread = threading.Thread(target=handleClient, args=(newClient,addr,))
        client_thread.start()
    

if __name__ == '__main__':
    main()


    