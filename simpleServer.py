#necessary packages
from socket import *

def main():

    #create a socket called server_sd
    server_sd = socket(AF_INET, SOCK_STREAM)

    #define how the client can connect
    port = 13400
    server_ip = '172.20.35.32' #10.47.15.70
    #bind the address to the socket
    server_sd.bind((server_ip,port))
    #wait for connection and create a new socket conn_sd for that connection
    #activate listening on the socket
    print("Listening for client...")
    server_sd.listen(1)
    #server waits on accept() for incoming
    #requests new socket created on return
    conn_sd, addr = server_sd.accept()
    #read data from the client and print
    recieved_line = conn_sd.recv(1024).decode()
    print(recieved_line)
    
    response = "Message recieved!"
    #send data back over the connection
    conn_sd.send(response.encode())


    #Closing code
    conn_sd.close()
    server_sd.close()

if __name__=='__main__':
    main()