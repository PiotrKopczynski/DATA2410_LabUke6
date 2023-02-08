#necessary packages
from socket import *

def main():
    message = "Hello world"

    #Create a socket called client_sd
    client_sd = socket(AF_INET, SOCK_STREAM)
    #Identify the server that you want to contact
    server_ip = '10.47.15.70'
    port = 12222
    #Connect to the server
    client_sd.connect((server_ip, port))
    #Send data
    client_sd.send(message.encode())

    #Read the data from the socket
    recieved_line = client_sd.recv(1024).decode()

    #print
    print(recieved_line)


    #closing code
    client_sd.close()