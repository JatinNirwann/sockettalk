# Server & Client Chat

A simple multi-client chat application where clients can send messages to each other through a central server. The server handles multiple clients and ensures messages are broadcasted to all connected users, excluding the sender.

## Features
- Supports multiple clients simultaneously
- Broadcasts messages to all clients except the sender
- Displays the sender's name with each message
- Notifies when a client joins or leaves the chat
- Server-side input for sending messages to all clients

## Technologies Used
- Python
- Sockets
- Threading

## How It Works
1. The server listens for incoming connections.
2. When a client connects, they provide a display name.
3. Messages sent by clients are prefixed with their display name and broadcast to all other clients.
4. The server can also send messages to all clients.
5. When a client disconnects, the server notifies all remaining clients.

## Firewall Rules
To allow external connections to the server, the following Windows Firewall rules were added:
- **Inbound Rule:** Allows TCP traffic on the specified port (e.g., 9090) for incoming connections.
- **Outbound Rule:** Allows TCP traffic on the specified port to enable responses to connected clients.
- **ICMPv6 (Echo Request):** Enabled to allow IPv6 ping requests.
- **Scope:** Configured to allow connections from any remote IP for broader access.

For now, I am using IPv6 because I am locked behind CG-NAT by my ISP. I might update this to use IPv4 later.

## Notes
- Ensure all clients connect to the correct server IP and port.
- The server must be running before clients can connect.
- Use `Ctrl+C` to stop the server.

Happy chatting! 🚀

