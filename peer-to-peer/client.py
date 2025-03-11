# client.py
import socket
import json
import threading
import time
import sys

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 0))  # Bind to any available port
local_port = sock.getsockname()[1]
print(f"Client bound to local port {local_port}")

# Default server address (using playit.gg)
DEFAULT_SERVER_HOST = 'floor-fighter.gl.at.ply.gg'
DEFAULT_SERVER_PORT = 54598
server_addr = (DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT)

client_id = None    # Will be set by user
peers = {}          # Will store peer information

# Helper function to parse address strings
def parse_address(addr_str):
    try:
        # Handle the case where addr might be formatted as "('ip', port)"
        if addr_str.startswith("(") and addr_str.endswith(")"):
            return eval(addr_str)
        
        # Handle the case where it's just "ip:port"
        if ":" in addr_str:
            host, port = addr_str.split(":")
            return (host, int(port))
            
        # Try parsing a comma separated format
        parts = addr_str.strip("()' ").replace("'", "").split(",")
        if len(parts) == 2:
            ip = parts[0].strip()
            port = int(parts[1].strip())
            return (ip, port)
    except:
        print(f"Warning: Couldn't parse address string: {addr_str}")
        return None
    
    return None

# Listener thread to handle incoming messages
def listener():
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = json.loads(data.decode())
            
            # Message from the server
            if addr == server_addr or addr[0] == server_addr[0]:
                if msg.get('status') == 'registered':
                    public_addr = msg.get('your_addr')
                    if isinstance(public_addr, str):
                        public_addr = parse_address(public_addr)
                    print(f"Registered with server. Public endpoint: {public_addr}")
                
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
                    
                    # Parse the address if it's a string
                    if isinstance(target_addr, str):
                        parsed_addr = parse_address(target_addr)
                        if parsed_addr:
                            target_addr = parsed_addr
                    
                    peers[target_id] = target_addr
                    print(f"Got address for {target_id}: {peers[target_id]}")
                    
                    # Start sending hole punching packets
                    threading.Thread(target=punch_hole, args=(target_id,)).start()
                
                elif msg.get('status') == 'connect_request':
                    from_id = msg.get('from_id')
                    from_addr = msg.get('from_addr')
                    
                    # Parse the address if it's a string
                    if isinstance(from_addr, str):
                        parsed_addr = parse_address(from_addr)
                        if parsed_addr:
                            from_addr = parsed_addr
                    
                    peers[from_id] = from_addr
                    print(f"Received connection request from {from_id} at {peers[from_id]}")
                    
                    # Start sending hole punching packets
                    threading.Thread(target=punch_hole, args=(from_id,)).start()
                
                elif msg.get('status') == 'error':
                    print(f"Error from server: {msg.get('message', 'Unknown error')}")
            
            # Direct message from a peer
            else:
                peer_id = None
                for pid, paddr in peers.items():
                    if paddr == addr:
                        peer_id = pid
                        break
                
                if msg.get('type') == 'punch':
                    print(f"Received punch from {'unknown' if peer_id is None else peer_id} at {addr}")
                    
                    # Send punch-ack back
                    sock.sendto(json.dumps({'type': 'punch_ack', 'from': client_id}).encode(), addr)
                    
                    # Add to peers if not already there
                    if peer_id is None:
                        peer_id = msg.get('from')
                        if peer_id:
                            peers[peer_id] = addr
                            print(f"Added new peer {peer_id} at {addr}")
                
                elif msg.get('type') == 'punch_ack':
                    print(f"Received punch acknowledgment from {'unknown' if peer_id is None else peer_id} at {addr}")
                    
                    # Add to peers if not already there
                    if peer_id is None:
                        peer_id = msg.get('from')
                        if peer_id:
                            peers[peer_id] = addr
                            print(f"Added new peer {peer_id} at {addr}")
                
                elif msg.get('type') == 'message':
                    print(f"Message from {msg.get('from', 'unknown')}: {msg.get('content', '')}")
        
        except Exception as e:
            print(f"Error in listener: {e}")

# Function to punch a hole to a peer
def punch_hole(peer_id):
    if peer_id not in peers:
        print(f"No address for peer {peer_id}")
        return
    
    peer_addr = peers[peer_id]
    print(f"Punching hole to {peer_id} at {peer_addr}")
    
    # Send several hole punching packets with increased frequency and count
    for i in range(15):  # Increased number of attempts
        try:
            sock.sendto(json.dumps({'type': 'punch', 'from': client_id}).encode(), peer_addr)
            print(f"Punch attempt {i+1}/15 to {peer_id}")
        except Exception as e:
            print(f"Error sending punch packet: {e}")
        time.sleep(0.2)  # Faster rate for more aggressive hole punching

# Main function
def main():
    global client_id
    
    # No command line args needed since server address is hardcoded
    print(f"Connecting to server at {DEFAULT_SERVER_HOST}:{DEFAULT_SERVER_PORT}")
    client_id = input("Enter a unique client ID: ")
    
    # Start the listener thread
    threading.Thread(target=listener, daemon=True).start()
    
    # Register with server
    print("Registering with server...")
    register_msg = {'action': 'register', 'id': client_id}
    sock.sendto(json.dumps(register_msg).encode(), server_addr)
    
    # Main command loop
    while True:
        print("\nCommands:")
        print("  list - List available clients")
        print("  connect <id> - Connect to a client")
        print("  send <id> <message> - Send message to a connected peer")
        print("  ping - Test server connection")
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
                try:
                    sock.sendto(json.dumps(msg).encode(), peers[peer_id])
                    print(f"Message sent to {peer_id}")
                except Exception as e:
                    print(f"Error sending message: {e}")
            else:
                print(f"Peer {peer_id} not connected. Use 'connect {peer_id}' first.")
        
        elif cmd[0] == 'ping':
            print("Pinging server...")
            ping_msg = {'action': 'list', 'id': client_id}  # Use list action as a ping
            sock.sendto(json.dumps(ping_msg).encode(), server_addr)
        
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()