import socket
import threading

HOST = "127.0.0.1"
PORT = 12341

def recieve_message(active_socket):
    while True: 
        data = active_socket.recv(1024)
        if not data:
            break
        print(f"{data.decode()}")

def main():
    username = input("Enter your username: ")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', PORT))
        thread = threading.Thread(target=recieve_message, args=(s,))
        thread.start()

        s.sendall(username.encode("utf-8"))
        while True:
            message = input().encode("utf-8")
            s.sendall(message)
            if message == b"/quit":
                thread.join()
                break

if __name__ == "__main__":
    main()