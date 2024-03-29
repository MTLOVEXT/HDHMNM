import socket
import pickle
import subprocess

def receive_data(connection):
    return pickle.loads(connection.recv(1024))

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 12345))
        print("Connected to server")
    except socket.error as e:
        print("Error occurred while connecting to server:", e)
        return

    while True:
        data = receive_data(client_socket)
        if "start_game" in data and data["start_game"]:
            print("Starting game...")
            subprocess.Popen(["python", "main.py"])  # Khởi chạy main.py
            break
        elif "message" in data:
            print("Server:", data["message"])

    client_socket.close()

if __name__ == "__main__":
    main()
