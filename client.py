
import socket
import threading
import time

#declaring some constants

encoder = "ascii"
bytesize = 1024

#static server ip and ports , only uncomment these when you know what you doing
def get_global_ipv6():
    hostname = socket.gethostname()
    addresses = socket.getaddrinfo(hostname, None, socket.AF_INET6)

    for addr in addresses:
        ip = addr[4][0]
        if not ip.startswith("fe80") and not ip.startswith("::1") and not ip.startswith("fd"):
            return ip  # found a global ipv6 address
    return None

# the for loop in above block discards the ipv6 address which start with "fe80","::1","fd" because these adresses can not be accessed globally 
ipv6 = get_global_ipv6()
if ipv6:
    server_ip = ipv6
else:
    print("Can not find global IPV6 addr")
server_port = 9090

# server_ip = input("Enter the IP of server you wish to connect to : ")
# server_port = input("Enter server port number : ")
displayname = input("Enter your Display name : ")

client_socket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
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