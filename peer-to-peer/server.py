# ===== MINIMAL CENTRAL SERVER FOR PLAYIT.GG =====
# server.py
import socket
import json

# Server configuration
LOCAL_HOST = '0.0.0.0'  # Listen on all interfaces
LOCAL_PORT = 12345      # Your specified local port
PUBLIC_HOST = 'floor-fighter.gl.at.ply.gg'  # Your playit.gg domain
PUBLIC_PORT = 54598     # Your playit.gg port

def run_server():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LOCAL_HOST, LOCAL_PORT))
    
    print(f"Server running locally on {LOCAL_HOST}:{LOCAL_PORT}")
    print(f"Server publicly accessible at {PUBLIC_HOST}:{PUBLIC_PORT} (via playit.gg)")
    
    # Dictionary to store client info
    clients = {}
    
    while True:
        # Receive data
        data, addr = sock.recvfrom(1024)
        try:
            msg = json.loads(data.decode())
            client_id = msg.get('id')
            action = msg.get('action')
            
            # Register new client
            if action == 'register':
                clients[client_id] = addr
                print(f"Registered client {client_id} at {addr}")
                
                # Send back the client's public address (as seen by the server)
                response = {'status': 'registered', 'your_addr': addr}
                sock.sendto(json.dumps(response).encode(), addr)
            
            # List available clients
            elif action == 'list':
                # Send list of all clients except the requester
                other_clients = {cid: str(caddr) for cid, caddr in clients.items() if cid != client_id}
                response = {'status': 'success', 'clients': other_clients}
                sock.sendto(json.dumps(response).encode(), addr)
            
            # Connection request
            elif action == 'connect':
                target_id = msg.get('target_id')
                if target_id in clients:
                    target_addr = clients[target_id]
                    
                    # Tell the requester about the target
                    requester_msg = {'status': 'info', 'target_id': target_id, 'target_addr': str(target_addr)}
                    sock.sendto(json.dumps(requester_msg).encode(), addr)
                    
                    # Tell the target about the requester
                    target_msg = {'status': 'connect_request', 'from_id': client_id, 'from_addr': str(addr)}
                    sock.sendto(json.dumps(target_msg).encode(), target_addr)
                    
                    print(f"Connection initiated: {client_id} -> {target_id}")
                else:
                    response = {'status': 'error', 'message': f"Client {target_id} not found"}
                    sock.sendto(json.dumps(response).encode(), addr)
        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_server()