import socket
import threading
import datetime

PORT = 12341
users = {}

time = datetime.datetime

keywords = [b"/quit", b"/list"]

def display_message_all(message):
    timestamp = str(time.now())
    for user in users.keys():
        user.sendall(timestamp.encode() + message)

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
        if data == b"/list":
            username_list = list(users.values())
            conn.sendall(b"\n".join(username_list))
        if not data:
            display_message_all(username + b" disconnected")
            users.pop(conn)
            break
        if not data in keywords:
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