from socket import * 
import threading
import _thread as thread
import time
import sys


gameStartMessage = "The game has started! You are playing against: "
gameWinMessage = "Congratulations! You won! :D"
gameLoseMessage = "Better luck next time ;("
gameDrawMessage = "The game was a draw!"
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
    
    if len(players)==2:
        player1Name = nicknames[players.index(players[0])]
        player2Name = nicknames[players.index(players[1])]
        players[0].send((gameStartMessage+player2Name).encode)
        players[1].send((gameStartMessage+player1Name).encode)

        player1answer = players[0].recv(1024).decode()
        player2answer = players[1].recv(1024).decode()

        if player1answer==player2answer:
            players[0].send(gameDrawMessage.encode)
            players[1].send(gameDrawMessage.encode)
        elif player1answer == "rock":
            if player2answer == "scissors":
                players[0].send(gameWinMessage.encode)
                players[1].send(gameLoseMessage.encode)
            else:
                players[0].send(gameLoseMessage.encode)
                players[1].send(gameWinMessage.encode)
        elif player1answer == "scissors":
            if player2answer == "paper":
                players[0].send(gameWinMessage.encode)
                players[1].send(gameLoseMessage.encode)
            else:
                players[0].send(gameLoseMessage.encode)
                players[1].send(gameWinMessage.encode)
        elif player1answer == "paper":
            if player2answer == "rock":
                players[0].send(gameWinMessage.encode)
                players[1].send(gameLoseMessage.encode)
            else:
                players[0].send(gameLoseMessage.encode)
                players[1].send(gameWinMessage.encode)
    players = []


    
    
    #to be implemented
    time.sleep(2)
    for player in players:
        print("hei")


def handleClient(client, addr):
    """
    a client handler function
    """
    #Welcome message and nickname creation
    client.send("Nickname:".encode())
    nickname = client.recv(1024).decode()
    welcomeMessage = "Welcome " + nickname + "! You are now connected! :O "
    client.send(welcomeMessage.encode())
    nicknames.append(nickname)
    try:
        broadcast(nickname + " just joined the server! :O\n", clients)
    except:
        print("Nicknames list is empty!")
    clients.append(client)
    print("AMOUNT OF CURRENT USERS: ",len(clients))
    print(nicknames)

    while True:
        try:
            message = client.recv(1024).decode()
            print(addr,message)
            #client.send("Message was recieved!".encode())
            if message=="exit":
                #clients.remove(client)
                #client.close()
                break
            elif message=="play!":
                if len(players) < 2:
                    players.append(client)
                    game(players)
                else:
                    client.send("Game server is full ;(. Try again later.".encode())
            else:
                i = clients.index(client)
                broadcast( nicknames[i] + ": " + message, clients[0:i]+clients[i+1:len(clients)])

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
        sys.exit()
    
    serverSocket.listen(1)
    print("The server is open! :D")

    while True:
        newClient, addr = serverSocket.accept()
        print("SERVER CONNECTED TO BY ", addr)
        print(" AT ", now())
        client_thread = threading.Thread(target=handleClient, args=(newClient,addr,))
        client_thread.start()
    serverSocket.close()
    

if __name__ == '__main__':
    main()


    