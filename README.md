# Chat Server & Client

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

## Windows Firewall Rules
To allow communication between the server and clients, the following Windows Firewall rules need to be added:

1. **Allow Incoming Connections for the Server**
   - Open Windows Defender Firewall with Advanced Security.
   - Create a new **Inbound Rule**.
   - Select **Port** and click **Next**.
   - Choose **TCP** and enter the server port (e.g., `5000`).
   - Allow the connection and apply it to **Private** and **Public** networks.
   - Name the rule (e.g., `Chat Server Inbound`), then save.

2. **Allow Outgoing Connections for the Client**
   - Open Windows Defender Firewall with Advanced Security.
   - Create a new **Outbound Rule**.
   - Select **Port** and click **Next**.
   - Choose **TCP** and enter the client connection port (e.g., `5000`).
   - Allow the connection and apply it to **Private** and **Public** networks.
   - Name the rule (e.g., `Chat Client Outbound`), then save.

3. **Allow the Python Executable**
   - In Windows Defender Firewall, create a new **Inbound Rule**.
   - Choose **Program** and select the Python executable (`python.exe`).
   - Allow the connection and apply it to **Private** and **Public** networks.
   - Name the rule (e.g., `Allow Python`), then save.

These rules ensure that the server can receive connections and clients can send messages without being blocked by the firewall.

## Notes
- Ensure all clients connect to the correct server IP and port.
- The server must be running before clients can connect.
- Use `Ctrl+C` to stop the server.


