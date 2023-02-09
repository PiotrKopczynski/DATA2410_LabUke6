from socket import *
import threading

serverName = socket.gethostbyname(socket.gethostname())
port = 12222
addr = (serverName, port)

server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)
server.listen(1)

clients = []
aliases = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode())
            aliases.remove(alias)
            break


def main():
    
    while True:
        print("Server is running and listening ...")
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode())
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode())
        broadcast(f'{alias} has connected to the chat room'.encode())
        client.send("You are now connected!".encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    main()
