
import socket
import threading
import time

#declaring constats

#if ypu are testing this on local macine then use same value for the variable in client script 
server_ip = socket.gethostbyname(socket.gethostname()) 

server_port = 9090
encoder = "ascii"
bytesize = 1024

clients = []
nicknames =[]

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((server_ip,server_port))

server_socket.listen()

print(f"Server is listening on {server_ip}:{server_port}....\n")

def broadcast(message):
    for client in clients:
        client.send(message.encode(encoder))

def handle_clients(client_socket,client_address):
    while True:
        try:
            message= client_socket.recv(bytesize).decode(encoder)
            broadcast(message)
        
        except:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left ..")
            break



def server_message():
    while True:
        if clients:
            message = input("Type Here: ")
            broadcast(f"Server: {message}")
        else:
            time.sleep(2)

server_thread = threading.Thread(target=server_message)
server_thread.daemon = True
server_thread.start()


while True:
    client_socket , client_address = server_socket.accept()
    client_socket.send("NICKNAME".encode(encoder))
    nickname = client_socket.recv(bytesize).decode(encoder)
    print(f"Connected with {nickname}({client_address})")
    nicknames.append(nickname)
    clients.append(client_socket)

    broadcast(f"{nickname} joined ")
    client_socket.send(f"You are now connected to server ({server_ip})\n".encode(encoder))

    thread = threading.Thread(target=handle_clients,args=(client_socket,client_address))
    thread.start()



