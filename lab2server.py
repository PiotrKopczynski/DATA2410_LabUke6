from socket import * 
import threading
import _thread as thread
import time

clients = []
nicknames = []
players = []

def now():
    """
    returns time of day
    """
    return time.ctime(time.time())

def broadcast(message, clientList):
    for client in clientList:
        client.send(message.encode())

def game(players):
    gameStartMessage = "The game has started! You are playing against: "
    gameWinMessage = "Congratulations! You won! :D"
    gameLoseMessage = "Better luck next time ;("
    while True:
        if len(players)==2:
            player1Name = nicknames[players.index(players[0])]
            player2Name = nicknames[players.index(players[1])]
            players[0].send((gameStartMessage+player2Name).encode)
            players[1].send((gameStartMessage+player1Name).encode)

    #to be implemented
    time.sleep(2)
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
            client.send("Message was recieved!".encode())
            if message=="exit":
                #clients.remove(client)
                #client.close()
                break
            elif message=="play!":
                if len(players) < 2:
                    players.append(client)
                else:
                    client.send("Game server is full ;(. Try again later.".encode())
        except:
            #remove the client and broadcast
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            leaveMessage = nickname + " has left the server ;(."
            broadcast(leaveMessage, clients)
            nicknames.remove(nickname)
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
        newClient.send("Nickname:".encode())
        nickname = newClient.recv(1024).decode()
        welcomeMessage = "Welcome " + nickname + "! You are now connected! :O "
        newClient.send(welcomeMessage.encode())
        nicknames.append(nickname)
        print("SERVER CONNECTED TO BY ", addr)
        print(" AT ", now())
        try:
            broadcast(nicknames[len(nicknames)-1]+" just joined the server! :O\n", clients)
        except:
            print("Nicknames list is empty!")
        clients.append(newClient)
        print("AMOUNT OF CURRENT USERS: ",len(clients))

        client_thread = threading.Thread(target=handleClient, args=(newClient,addr,))
        client_thread.start()
    

if __name__ == '__main__':
    main()


    