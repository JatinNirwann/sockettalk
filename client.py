
import socket
import threading
import time

#declaring some constants

encoder = "ascii"
bytesize = 1024

#static server ip and ports , only uncomment these when you know what you doing
server_ip = socket.gethostbyname(socket.gethostname()) 
server_port = 9090

# server_ip = input("Enter the IP of server you wish to connect to : ")
# server_port = input("Enter server port number : ")
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
                print(message)
        except:
            print("We are having trouble reading data from server ...try re-establishing connection with server")
            client_socket.close()
            break


def send():
    while True:
        try:
            message = input() 
            client_socket.send(message.encode(encoder))
        except Exception as e:
            print(f"Error while sending message: {e}")
            client_socket.close()
            break

def main():
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    send_thread = threading.Thread(target=send)
    send_thread.start()

if __name__ == "__main__":
    main()