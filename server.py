import socket
import threading
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = int(os.environ.get("PORT", 10000))
server.bind(('0.0.0.0', PORT))
server.listen()

clients = []

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
              
                client.sendall(message)
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"Connected: {addr}")
    while True:
        try:
            data = conn.recv(1024 * 1024) 
            if not data: break
            broadcast(data, conn)
        except: break
    conn.close()

print("Server is ready...")
while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
