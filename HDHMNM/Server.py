import subprocess
import socket
import threading

MAX_CONNECTIONS = 2
connections = []

def handle_connection(conn, addr):
    global connections
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            for c in connections:
                if c != conn:  # Gửi dữ liệu cho tất cả các client khác ngoại trừ chính client gửi tin nhắn
                    c.sendall(data)
    except Exception as e:
        print("Error occurred while handling connection:", e)
    finally:
        connections.remove(conn)
        conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(MAX_CONNECTIONS)
    print("Server is waiting for connections...")

    while len(connections) < MAX_CONNECTIONS:
        conn, addr = server_socket.accept()
        connections.append(conn)
        print("Connected to client", len(connections))
        if len(connections) == MAX_CONNECTIONS:
            print("Starting the game...")
            server_socket.close()
            subprocess.run(["python", "main.py"])

if __name__ == "__main__":
    start_server()
