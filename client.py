
import socket
import threading

#declaring some constants

encoder = "ascii"
bytesize = 1024

server_ip = input("Enter the IP of server you wish to connect to : ")
server_port = input("Enter server port number : ")
displayname = input("Enter your Display name : ")

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((server_ip,int(server_port)))

def receive():
    while True:
        try:
            message =client_socket.recv(bytesize).decode(encoder)
            if message == "NICKNAME":
                client_socket.send(displayname.encode(encoder))
            else:
                print(f"Server:{message}")
        except:
            print("We are having trouble reading data from server .....try re-establishing connection with server")
            client_socket.close()
            break

def send():
    while True:
            message =input("Type Below : \n")
            client_socket.send(message.encode(encoder))

def main():
    
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    send_thread = threading.Thread(target=send)
    send_thread.start()
