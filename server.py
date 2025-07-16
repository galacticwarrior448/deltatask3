import socket
import threading
import time
import mysql.connector

HOST = '0.0.0.0'
PORT = 12345

clients = {}  # client_socket: (username, room)
rooms = {}    # room_name: [client_sockets]
users = {}    # username: [time_spent, messages_sent]


#db = mysql.connector.connect(host='mysql', port=3306, user='root', password='password')
#cursor = db.cursor()
#cursor.execute("CREATE DATABASE IF NOT EXISTS userdata")
#cursor.execute("USE userdata")
#cursor.execute("CREATE TABLE IT NOT EXISTS users(username VARCHAR(255) PRIMARY KEY UNIQUE,time_spent INT, messages_sent INT)")
#cursor.execute("CREATE TABLE IT NOT EXISTS rooms(roomname VARCHAR(255) PRIMARY KEY UNIQUE)")
#cursor.execute("CREATE TABLE IT NOT EXISTS roomusers(username VARCHAR(255), roomname VARCHAR(255), FOREIGN KEY (username) REFERENCES users(username), FOREIGN KEY (roomname) REFERENCES rooms(roomname))")

def counttime(user, exit_status):
    while exit_status != True:
        users[user][0] += 1
        time.sleep(1)

def broadcast(msg, room, sender_socket):
    for client in rooms.get(room, []):
        if client != sender_socket:
            try:
                client.sendall(msg.encode())
            except:
                pass 

def handle_client(client_socket):
    try:
        client_socket.send(b'Enter your username: ')
        start_time = time.time()
        username = client_socket.recv(1024).decode().strip()
        client_socket.send(b'Create or join a room using /create <room> or /join <room>\n')
        time_spent, messages_sent = users.get(username, (0, 0))
        users.setdefault(username, [0, 0])
        exit_status = False
        threading.Thread(target=counttime, args=(username,exit_status), daemon=True).start()


        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            msg = data.decode().strip()
            
            if msg.startswith("/create "):
                user, oldroom = clients.get(client_socket, (None, None))
                room = msg.split()[1]
                rooms.setdefault(room, []).append(client_socket)
                clients[client_socket] = (username, room)
                client_socket.send(f'Room {room} created and joined!\n'.encode())
                if oldroom:
                    rooms[oldroom].remove(client_socket)
            elif msg.startswith("/join "):
                user, oldroom = clients.get(client_socket, (None, None))
                room = msg.split()[1]
                if room not in rooms:
                    client_socket.send(b'Room does not exist.\n')
                    continue
                rooms[room].append(client_socket)
                clients[client_socket] = (username, room)
                client_socket.send(f'Joined room {room}\n'.encode())
                if oldroom:
                    rooms[oldroom].remove(client_socket)
                
            elif msg.startswith("/list"):
                room_list = ", ".join(rooms.keys())
                client_socket.send(f'Available rooms: {room_list}\n'.encode())
            elif msg.startswith("/quit"):
                user, oldroom = clients.get(client_socket, (None, None))
                if oldroom:
                    rooms[oldroom].remove(client_socket)
                break
            elif msg.startswith("/stats"):
                user_list = [clients[sock][0] for sock in rooms[room]]
                print(user_list)
                user_str = ", ".join(user_list)
                print(user_str)
                print(users)
                client_socket.send(f"Number of users in Room:{room} is {len(rooms[room])}. Users in this room are: {user_str}".encode())
                client_socket.send(f"Your stats are :\n messages sent =   {users[user][1]}\n time spent ={users[user][0]} seconds".encode())
                
            else:
                user, room = clients.get(client_socket, (None, None))
                if room:
                    broadcast(f'{user}: {msg}', room, client_socket)
                    users[user][1] += 1
                else:
                    client_socket.send(b'Join a room first!\n')
    except:
        pass
    finally:
        exit_status=False
        end_time = time.time()
        user, room = clients.pop(client_socket, (None, None))
        users[user][0] += end_time-start_time
        if room and client_socket in rooms.get(room, []):
            rooms[room].remove(client_socket)
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server running on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    main()

