import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 12345

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    threading.Thread(target=receive, args=(client_socket,), daemon=True).start()

    try:
        while True:
            msg = input()
            if msg == "/exit":
                client_socket.send(b'/quit')
                break
            client_socket.send(msg.encode())
    except KeyboardInterrupt:
        client_socket.send(b'/quit')

    client_socket.close()

if __name__ == "__main__":
    main()

