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

## Setup & Usage

### Running the Server
1. Open a terminal and navigate to the project folder.
2. Run the server script:
   ```sh
   python server.py
   ```
3. The server will start listening for connections.

### Running the Client
1. Open another terminal and navigate to the project folder.
2. Run the client script:
   ```sh
   python client.py
   ```
3. Enter the server's IP address and port when prompted.
4. Enter a display name and start chatting!

### Example Interaction
```
Alice: Hello everyone!
Bob: Hi Alice!
Server: Welcome to the chat!
```

## Notes
- Ensure all clients connect to the correct server IP and port.
- The server must be running before clients can connect.
- Use `Ctrl+C` to stop the server.

Happy chatting! 🚀

