#to install this run "pip install pystun3"

import stun

stun_servers = [
    "stun.l.google.com", 
    "stun1.l.google.com",
    "stun2.l.google.com",
    "stun3.l.google.com",
    "stun4.l.google.com",
    "stun.ekiga.net",
    "stun.ideasip.com",
    "stun.sipgate.net",
    "stun.voipstunt.com"
]

for server in stun_servers:
    try:
        print(f"Trying STUN server: {server}")
        nat_type, external_ip, external_port = stun.get_ip_info(stun_host=server)
        if external_ip:
            print(f"NAT Type: {nat_type}")
            print(f"Your Public IP: {external_ip}, Port: {external_port}")
            break
    except Exception as e:
        print(f"Failed with {server}: {e}")