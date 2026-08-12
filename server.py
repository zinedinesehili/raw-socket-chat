import socket
import threading

PORT = 12342
users = {}

def display_message_all(message):
    for user in users:
        users[user].sendall(message)

def handle_client(conn, addr):
    username = conn.recv(1024)
    users[username] = conn

    display_message_all(username + b" connected")

    while True:
        data = conn.recv(1024)
        if data == b"/quit":
            display_message_all(username + b" disconnected")
            conn.close()
            users.pop(username)
            break
        if not data:
            display_message_all(username + b" disconnected")
            users.pop(username)
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