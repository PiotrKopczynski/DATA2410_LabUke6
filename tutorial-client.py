from socket import *
import threading

serverName = socket.gethostbyname(socket.gethostname())
port = 12222
addr = (serverName, port)

alias = input('Choose an alias >>>')
client = socket(AF_INET, SOCK_STREAM)
client.connect(addr)

def client_recieve():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "alias?":
                client.send(alias.encode())
            else:
                print(message)
        except:
            print("Error!")
            client.close()
            break

def client_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode())

recieve_thread = threading.Thread(target=client_recieve)
recieve_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
