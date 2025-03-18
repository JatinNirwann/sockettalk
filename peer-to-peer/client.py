import socket
import json
import threading
import time
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 0)) 
local_port = sock.getsockname()[1]
print(f"Client bound to local port {local_port}")

server_addr = None 
client_id = None    
peers = {}         

def listener():
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = json.loads(data.decode())
            
            if addr == server_addr:
                if msg.get('status') == 'registered':
                    print(f"Registered with server. Public endpoint: {msg.get('your_addr')}")
                
                elif msg.get('status') == 'success' and 'clients' in msg:
                    if not msg['clients']:
                        print("No other clients connected")
                    else:
                        print("Available clients:")
                        for cid, caddr in msg['clients'].items():
                            print(f"  {cid}: {caddr}")
                
                elif msg.get('status') == 'info':
                    target_id = msg.get('target_id')
                    target_addr = msg.get('target_addr')
                    peers[target_id] = eval(target_addr) if isinstance(target_addr, str) else target_addr
                    print(f"Got address for {target_id}: {peers[target_id]}")
                    
                    threading.Thread(target=punch_hole, args=(target_id,)).start()
                
                elif msg.get('status') == 'connect_request':
                    from_id = msg.get('from_id')
                    from_addr = msg.get('from_addr')
                    peers[from_id] = eval(from_addr) if isinstance(from_addr, str) else from_addr
                    print(f"Received connection request from {from_id} at {peers[from_id]}")
                    
                    threading.Thread(target=punch_hole, args=(from_id,)).start()
            
            else:
                peer_id = None
                for pid, paddr in peers.items():
                    if paddr == addr:
                        peer_id = pid
                        break
                
                if msg.get('type') == 'punch':
                    print(f"Received punch from {'unknown' if peer_id is None else peer_id} at {addr}")
                    
                    sock.sendto(json.dumps({'type': 'punch_ack', 'from': client_id}).encode(), addr)
                    
                    if peer_id is None:
                        peer_id = msg.get('from')
                        if peer_id:
                            peers[peer_id] = addr
                            print(f"Added new peer {peer_id} at {addr}")
                
                elif msg.get('type') == 'punch_ack':
                    print(f"Received punch acknowledgment from {'unknown' if peer_id is None else peer_id} at {addr}")
                    
                    if peer_id is None:
                        peer_id = msg.get('from')
                        if peer_id:
                            peers[peer_id] = addr
                            print(f"Added new peer {peer_id} at {addr}")
                
                elif msg.get('type') == 'message':
                    print(f"Message from {msg.get('from', 'unknown')}: {msg.get('content', '')}")
        
        except Exception as e:
            print(f"Error in listener: {e}")

def punch_hole(peer_id):
    if peer_id not in peers:
        print(f"No address for peer {peer_id}")
        return
    
    peer_addr = peers[peer_id]
    print(f"Punching hole to {peer_id} at {peer_addr}")
    
    for i in range(5):
        sock.sendto(json.dumps({'type': 'punch', 'from': client_id}).encode(), peer_addr)
        time.sleep(0.5)

def main():
    global server_addr, client_id
    
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <server_ip> <server_port>")
        sys.exit(1)
    
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    server_addr = (server_ip, server_port)
    
    client_id = input("Enter a unique client ID: ")
    
    threading.Thread(target=listener, daemon=True).start()
    
    register_msg = {'action': 'register', 'id': client_id}
    sock.sendto(json.dumps(register_msg).encode(), server_addr)
    
    while True:
        print("\nCommands:")
        print("  list - List available clients")
        print("  connect <id> - Connect to a client")
        print("  send <id> <message> - Send message to a connected peer")
        print("  exit - Exit the client")
        
        cmd = input("> ").strip().split()
        if not cmd:
            continue
        
        if cmd[0] == 'exit':
            break
        
        elif cmd[0] == 'list':
            list_msg = {'action': 'list', 'id': client_id}
            sock.sendto(json.dumps(list_msg).encode(), server_addr)
        
        elif cmd[0] == 'connect' and len(cmd) > 1:
            target_id = cmd[1]
            connect_msg = {'action': 'connect', 'id': client_id, 'target_id': target_id}
            sock.sendto(json.dumps(connect_msg).encode(), server_addr)
        
        elif cmd[0] == 'send' and len(cmd) > 2:
            peer_id = cmd[1]
            message = ' '.join(cmd[2:])
            
            if peer_id in peers:
                msg = {'type': 'message', 'from': client_id, 'content': message}
                sock.sendto(json.dumps(msg).encode(), peers[peer_id])
                print(f"Message sent to {peer_id}")
            else:
                print(f"Peer {peer_id} not connected. Use 'connect {peer_id}' first.")
        
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()