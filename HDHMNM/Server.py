import socket
import threading
import pickle
import sys

MAX_CONNECTIONS = 2
connections = []
ready_to_start = False

def handle_client(conn):
    global ready_to_start
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # Xử lý dữ liệu từ client nếu cần
    except Exception as e:
        print("Error occurred while handling connection:", e)
    finally:
        connections.remove(conn)
        conn.close()

def keyboard_listener():
    global ready_to_start
    while True:
        key = input("Press 'q' to quit: ")
        if key == 'q':
            print("Closing server...")
            for conn in connections:
                conn.close()
            sys.exit()

def main():
    global ready_to_start
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(MAX_CONNECTIONS)
    print("Server is waiting for connections...")

    threading.Thread(target=keyboard_listener, daemon=True).start()

    while True:
        conn, addr = server_socket.accept()
        connections.append(conn)
        print("Connected to client", len(connections))
        threading.Thread(target=handle_client, args=(conn,)).start()

        if len(connections) == MAX_CONNECTIONS and not ready_to_start:
            ready_to_start = True
            print("Ready to start game")
            for conn in connections:
                conn.send(pickle.dumps({"start_game": True}))

        if len(connections) > MAX_CONNECTIONS:
            conn.send(pickle.dumps({"message": "Too many connections, please try again later."}))
            conn.close()
            connections.remove(conn)

if __name__ == "__main__":
    main()
