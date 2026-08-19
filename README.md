# raw-socket-chat
A multi-client terminal chat server built from scratch using raw TCP sockets and threading in Python, without any frameworks or non-standard libraries.

## Features
- Multi client support via one thread per connected client
- Real-time broadcast messaging between all connected users
- Custom usernames
- `/list` - view all currently connected users
- `/quit` - disconnect cleanly from the chat
- Message timestamps
- Join/leave notifications broadcast to the room

## How to run
1. Start the server:
   ```
   python3 server.py
   ```
2. In a separate terminal, start a client:
   ```
   python3 client.py
   ```
3. Repeat step 2 in additional terminals to simulate multiple users. When prompted, enter the server's IP address (use `localhost` if running on the same machine).

**Tested with multiple terminal instances on one machine, as well as across two separate physical devices connected to the same Wi-Fi network.**

> **Note (Windows):** if running the server on Windows, make sure Python is allowed through Windows Firewall for both **Private** and **Public** networks (Settings → Windows Defender Firewall → "Allow an app through firewall"). Windows can silently block incoming connections on a private network otherwise.

## How it works
- The server listens on a socket and calls `accept()` in a loop, passing each new connection to its own thread (`handle_client`) so multiple clients can be handled concurrently without blocking one another
- Connections are tracked in a dictionary with each client's socket object (`conn`) as the key mapped to their username. This avoids collisions that a username-based key would risk if two users chose the same name.
- Broadcasting loops over all active connections to send messages to every client
- The client runs two independent loops: one for sending (reading user input and sending it) and one for receiving (in its own thread), so a client can receive messages at any time, not just right after sending one

## Known limitations
- Usernames aren't required to be unique, so the chat can get confusing if multiple users have the same name
- Messages are capped at 1024 bytes per receive call, so longer messages aren't handled gracefully
- No encryption; everything is sent in plain text

## What I learned
Building this from raw sockets allowed me to get a real hands-on understanding of TCP connections, concurrency, and the specific bugs that came from managing shared states and multiple threads (including diagnosing a live race condition between a client's sender and receiver threads).