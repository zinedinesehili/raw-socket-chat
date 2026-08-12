import socket
import threading

PORT = 12341
users = {}

def display_message_all(message):
    for user in users.keys():
        user.sendall(message)

def handle_client(conn, addr):
    username = conn.recv(1024)
    users[conn] = username

    display_message_all(username + b" connected")

    while True:
        data = conn.recv(1024)
        if data == b"/quit":
            display_message_all(username + b" disconnected")
            conn.close()
            users.pop(conn)
            break
        if not data:
            display_message_all(username + b" disconnected")
            users.pop(conn)
            break
        display_message_all(username + b": " + data)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', PORT))
        s.listen()
        print("Server is running")

        while True:
            conn, addr = s.accept()

            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()