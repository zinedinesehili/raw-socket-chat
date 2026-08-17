import socket
import threading
import datetime

PORT = 12340
users = {}

time = datetime.datetime

keywords = [b"/quit", b"/list"]

def format_timestamp(current_time):
    # TODO
    return

def display_message_all(message):
    current_time = time.now()
    year = str(current_time.year)
    month = str(current_time.month)
    day = str(current_time.day)
    hour = str(current_time.hour)
    minute = str(current_time.minute)
    timestamp = f"{day}/{month}/{year} {hour}:{minute:02}: "
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