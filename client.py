import socket
import threading

PORT = 12340

def recieve_message(active_socket):
    while True: 
        data = active_socket.recv(1024)
        if not data:
            break
        print(f"{data.decode()}")

def main():
    ip = input("Enter the address you want to connect to")
    username = input("Enter your username: ")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, PORT))
        thread = threading.Thread(target=recieve_message, args=(s,))
        thread.start()

        s.sendall(username.encode("utf-8"))
        while True:
            message = input()
            s.sendall(message.encode("utf-8"))
            if message == "/quit":
                thread.join()
                break

if __name__ == "__main__":
    main()