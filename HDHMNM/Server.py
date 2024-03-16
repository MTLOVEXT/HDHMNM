import socket
import pickle
import threading
import tkinter as tk

# Define global variables
MAX_CONNECTIONS = 2
BOARD_SIZE = 15
CELL_SIZE = 50
SCREEN_SIZE = (BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = 1
connections = []

def send_data(connection, data):
    connection.send(pickle.dumps(data))

def receive_data(connection):
    return pickle.loads(connection.recv(1024))

def create_board():
    global board
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def check_win(row, col):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # vertical, horizontal, diagonal, anti-diagonal

    for dr, dc in directions:
        count = 1
        for i in range(1, 5):
            r = row + dr * i
            c = col + dc * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == board[row][col]:
                count += 1
            else:
                break
        for i in range(1, 5):
            r = row - dr * i
            c = col - dc * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == board[row][col]:
                count += 1
            else:
                break
        if count >= 5:
            return True

    return False

def handle_connection(conn, addr):
    global current_player
    while True:
        try:
            move = receive_data(conn)
            board[move[0]][move[1]] = current_player

            if check_win(move[0], move[1]):
                print("Player", current_player, "wins!")
                send_data(conn, {"winner": current_player})
                for c in connections:
                    c.close()
                root.quit()
                return

            current_player = 3 - current_player
        except Exception as e:
            print("Error occurred while handling connection:", e)
            connections.remove(conn)
            break

def start_game():
    global root
    root = tk.Tk()
    root.title("Caro Server")

    create_board()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(MAX_CONNECTIONS)
    print("Server is waiting for connections...")

    while len(connections) < MAX_CONNECTIONS:
        conn, addr = server_socket.accept()
        connections.append(conn)
        print("Connected to client", len(connections))
        threading.Thread(target=handle_connection, args=(conn, addr)).start()

    root.mainloop()

if __name__ == "__main__":
    start_game()
