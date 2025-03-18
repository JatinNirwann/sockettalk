import socket
import json

def run_server(host='0.0.0.0', port=5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Server running on {host}:{port}")
    
    clients = {}
    
    while True:
        data, addr = sock.recvfrom(1024)
        try:
            msg = json.loads(data.decode())
            client_id = msg.get('id')
            action = msg.get('action')
            
            if action == 'register':
                clients[client_id] = addr
                print(f"Registered client {client_id} at {addr}")
                response = {'status': 'registered', 'your_addr': addr}
                sock.sendto(json.dumps(response).encode(), addr)
            
            elif action == 'list':
                other_clients = {cid: str(caddr) for cid, caddr in clients.items() if cid != client_id}
                response = {'status': 'success', 'clients': other_clients}
                sock.sendto(json.dumps(response).encode(), addr)
            
            elif action == 'connect':
                target_id = msg.get('target_id')
                if target_id in clients:
                    target_addr = clients[target_id]
                    
                    requester_msg = {'status': 'info', 'target_id': target_id, 'target_addr': target_addr}
                    sock.sendto(json.dumps(requester_msg).encode(), addr)
                    
                    target_msg = {'status': 'connect_request', 'from_id': client_id, 'from_addr': addr}
                    sock.sendto(json.dumps(target_msg).encode(), target_addr)
                    
                    print(f"Connection initiated: {client_id} -> {target_id}")
                else:
                    response = {'status': 'error', 'message': f"Client {target_id} not found"}
                    sock.sendto(json.dumps(response).encode(), addr)
        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_server()