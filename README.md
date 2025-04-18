# Server & Client Chat  

## ⚡ Planned Updates  
- Adding **peer-to-peer (P2P) communication** alongside the current client-server model.  
- Using a **public IP server** for initial connection and implementing **hole punching** for direct P2P communication.  
- **IPv6 as the primary method**, with **IPv4 as a fallback**.  
- Removing **IPv6 and firewall details** from the client-server setup once P2P is implemented.  
- **Integrating both methods into one app**, allowing users to choose between client-server or P2P communication.
- Create a **web interface** using Flask/FastAPI to replace the command-line interface
- Implement **WebSocket protocol** for real-time browser communication
- Develop a **responsive web UI** with chat window, message input, and user list

## Features  
- Supports multiple clients simultaneously  
- Broadcasts messages to all clients except the sender  
- Displays the sender's name with each message  
- Notifies when a client joins or leaves the chat  
- Server-side input for sending messages to all clients  
- Future support for both client-server and P2P communication modes

## Notes  
- Ensure all clients connect to the correct server IP and port.  
- The server must be running before clients can connect.  
- Use `Ctrl+C` to stop the server.  
- Web interface will provide an alternative to CLI for easier access