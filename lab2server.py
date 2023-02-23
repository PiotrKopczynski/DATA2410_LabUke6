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
clients = [] #array containing client sockets
nicknames = [] #array containing string nicknames of clients
players = [] #array containing client sockets that are used in the game function
gameAnswers = {} #dictionary containing string answers used in the game function

def now():
    """
    Function: Finds time of day and returns it.
    """
    return time.ctime(time.time())

def broadcast(message, clientList):
    """
    Function: Encodes and sends a message to clients in clientList.
    Input: A message string to be sent and an array containing client sockets.
    """
    for client in clientList:
        client.send(message.encode())

def game(players, gameAnswers):
    """
    Function: Lets two clients play a game of rock, paper, scissors.
    Input: Array containing client sockets of clients playing the game, and a dictionary containing nicknames as keys
    and strings as values.
    Returns: This function does not return anything.
    Exceptions: The only exception handled in this function is the case when one or both players
    leave at any point during the game. The function contains an if statements that checks if the
    number of players is not correct, then the game clears the player and gameAnswer arrays and then
    terminates.
    """
    while True:
        if len(players) != 1:
            players.clear()
            gameAnswers.clear()
            return
        players[0].send(gameWaitMessage.encode()) #Tells the players that they are waiting for an opponent.
        time.sleep(4)
        if len(players)==2:
            player1Name = nicknames[clients.index(players[0])]
            player2Name = nicknames[clients.index(players[1])]
            players[0].send((gameStartMessage+player2Name).encode())
            players[1].send((gameStartMessage+player1Name).encode())

            while True: #This loop waits for answers from both players
                    if len(players) != 2:
                        players.clear()
                        gameAnswers.clear()
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


def handleClient(client, addr):
    """
    Function: A client handler function that also lets a client join a game of rock, paper, scissors andcan start a 
    new thread running the game function if a recognised request is recieved from the client.
    Inputs: A client socket and its address.
    Returns: Returns nothing.
    Exceptions: This function handles the exception if there are errors recieving from or sending messages to the client.
    This happens in a try except block, where the except block will remove the client information from all arrays, sends
    a broadcast that the client has left lastly breaks the loop such that the thread stops.
    """
    #Welcome message and nickname creation
    client.send("Nickname:".encode())
    nickname = client.recv(1024).decode()
    welcomeMessage = "Welcome " + nickname + "! You are now connected! :O Write play! to join a game of rock, paper scissors :D"
    client.send(welcomeMessage.encode())
    nicknames.append(nickname)
    broadcast(nickname + " just joined the server! :O\n", clients) # The client array here does not contain the new client yet
    clients.append(client)
    print("AMOUNT OF CURRENT USERS: ", len(clients)) 

    while True:
        try:
            message = client.recv(1024).decode()
            print(addr,message) #Prints the message on the server side to keep track of the traffic
            if message=="play!":
                if len(players) < 2 and client not in players:
                    players.append(client) # Adds the client to the player array
                    if len(players) == 1: # If at least one client wants to play a game thread is created
                        game_thread = threading.Thread(target=game, args=(players, gameAnswers,))
                        game_thread.start()
                else:
                    client.send("Game server is full ;(. Try again later.".encode())
            elif client in players and (message == "rock" or message == "scissors" or message == "paper"):
                gameAnswers[nickname] = message
            else:
                if message != "exit":
                    i = clients.index(client)
                    broadcast(now() + " " + nickname + ": " + message, clients[0:i]+clients[i+1:len(clients)])

        except: #remove the client information and broadcast to the rest
            index = clients.index(client)
            clients.remove(client)

            if client in players:
                players.remove(client)

            client.close()

            nickname = nicknames[index] # nickname of the removed client
            leaveMessage = nickname + " has left the server ;(."
            broadcast(leaveMessage, clients)
            nicknames.remove(nickname)
            break





def main():
    """
    Function: Creates a server socket, listens for new connections and spwans a new thread whenever a new
    connection joins.
    Exceptions: The function handles the exception if the bind to the socket failed in a try except block.
    In this case the functions gives av error message and exits the program.
    """
    serverPort = 12220
    serverName = gethostbyname(gethostname()) # This function automatically fetches the local IP
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


    