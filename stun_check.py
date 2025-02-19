import stun

stun_host = "stun.l.google.com"
stun_port = 19302  # Google's STUN Server

nat_type, external_ip, external_port = stun.get_ip_info(stun_host=stun_host, stun_port=stun_port)

print(f"NAT Type: {nat_type}")
print(f"Your Public IP: {external_ip}, Port: {external_port}")
