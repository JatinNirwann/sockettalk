#this file contains blocks of test code for debuging 

import socket

server_ip = "2401:4900:1f30:439e:e80f:aeac:dff7:741a"  # Replace with actual IPv6 address
server_port = 9090

server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()

print(f"Server is listening on {server_ip}:{server_port}....\n")
