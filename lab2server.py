from socket import * 
import threading
import _thread as thread
import time
import sys


gameStartMessage = "The game has started! You are playing against: "
gameWinMessage = "Congratulations! You won! :D"
gameLoseMessage = "Better luck next time ;("
gameDrawMessage = "The game was a draw!"
gameWaitMessage = "Waiting for an opponent..."
clients = []
nicknames = []
players = []
gameAnswers = {}
stopGame = False


def now():
    """
    returns time of day
    """
    return time.ctime(time.time())

def broadcast(message, clientList):
    for client in clientList:
        client.send(message.encode())

def game(players, gameAnswers):
    while True:
        if len(players) == 0:
            return
        players[0].send(gameWaitMessage.encode())
        time.sleep(4)
        if len(players)==2:
            player1Name = nicknames[clients.index(players[0])]
            player2Name = nicknames[clients.index(players[1])]
            players[0].send((gameStartMessage+player2Name).encode())
            players[1].send((gameStartMessage+player1Name).encode())

            while True:
                    if len(players) == 1:
                        return
                    broadcast("Waiting for answers...",players)
                    time.sleep(5)
                    if len(gameAnswers) == 2:
                        break


            player1answer = gameAnswers[player1Name]
            player2answer = gameAnswers[player2Name]

            if player1answer==player2answer:
                players[0].send(gameDrawMessage.encode())
                players[1].send(gameDrawMessage.encode())
            elif player1answer == "rock":
                if player2answer == "scissors":
                    players[0].send(gameWinMessage.encode())
                    players[1].send(gameLoseMessage.encode())
                else:
                    players[0].send(gameLoseMessage.encode())
                    players[1].send(gameWinMessage.encode())
            elif player1answer == "scissors":
                if player2answer == "paper":
                    players[0].send(gameWinMessage.encode())
                    players[1].send(gameLoseMessage.encode())
                else:
                    players[0].send(gameLoseMessage.encode())
                    players[1].send(gameWinMessage.encode())
            elif player1answer == "paper":
                if player2answer == "rock":
                    players[0].send(gameWinMessage.encode())
                    players[1].send(gameLoseMessage.encode())
                else:
                    players[0].send(gameLoseMessage.encode())
                    players[1].send(gameWinMessage.encode())
            players.clear()
            gameAnswers.clear()
            return


#def clean(client):


def handleClient(client, addr):
    """
    a client handler function
    """
    #Welcome message and nickname creation
    client.send("Nickname:".encode())
    nickname = client.recv(1024).decode()
    welcomeMessage = "Welcome " + nickname + "! You are now connected! :O Write play! to join a game of rock, paper scissors :D"
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
            #if message=="exit":
                #clients.remove(client)
                #client.close()
                #break
            if message=="play!":
                print(len(players))
                if len(players) < 2 and client not in players:
                    players.append(client)
                    if len(players) == 1:
                        game_thread = threading.Thread(target=game, args=(players, gameAnswers,))
                        game_thread.start()
                else:
                    client.send("Game server is full ;(. Try again later.".encode())
            elif client in players and (message == "rock" or message == "scissors" or message == "paper"):
                gameAnswers[nickname] = message
            else:
                i = clients.index(client)
                broadcast(nickname + ": " + message, clients[0:i]+clients[i+1:len(clients)])

        except:
            #remove the client and broadcast
            index = clients.index(client)
            clients.remove(client)
            if client in players:
                players.remove(client)
            client.close()
            nickname = nicknames[index]
            leaveMessage = nickname + " has left the server ;(."
            broadcast(leaveMessage, clients)
            nicknames.remove(nickname)
            break





def main():

    serverPort = 12220
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


    