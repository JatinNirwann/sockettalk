
import socket
import threading

#declaring constats

server_ip = socket.gethostbyname(socket.gethostname())
server_port = 9090
encoder = "ascii"
bytesize = 1024

clients = []
nicknames =[]

def broadcast():
    for clients in clients:
        client_socket.send(message.encode(encoder))

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



server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((server_ip,server_port))

server_socket.listen()

print(f"Server is listening on {server_ip}:{server_port}....\n")

client_socket , client_address = server_socket.accept()
client_socket.send("NICKNAME".encode(encoder))
nickname = client_socket.recv(bytesize).decode(encoder)
print(f"Client {nickname} connected from {client_address}")
client_socket.send(f"You are now connected to server ({server_ip})\n".encode(encoder))
client_socket.send("NICKNAME".encode(encoder))


while True:
    message = client_socket.recv(bytesize).decode(encoder)

    print(f"\n Client:  {message}")
    message=input("Type Here: ")
    client_socket.send(message.encode(encoder))
