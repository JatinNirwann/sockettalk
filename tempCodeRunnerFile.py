def get_global_ipv6():
#     hostname = socket.gethostname()
#     addresses = socket.getaddrinfo(hostname, None, socket.AF_INET6)

#     for addr in addresses:
#         ip = addr[4][0]
#         if not ip.startswith("fe80") and not ip.startswith("::1") and not ip.startswith("fd"):
#             return ip  # found a global ipv6 address
#     return None

# # the for loop in above block discards the ipv6 address which start with "fe80","::1","fd" because these adresses can not be accessed globally 
# ipv6 = get_global_ipv6()
# if ipv6:
#     server_ip = ipv6
# else:
#     print("Can not find global IPV6 addr")