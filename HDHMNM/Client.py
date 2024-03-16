import socket
import pickle
import tkinter as tk
from tkinter import messagebox

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Define cell and board sizes
CELL_SIZE = 40
BOARD_SIZE = 15
SCREEN_SIZE = (BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)

# Define functions to draw board and pieces
def draw_board(screen):
    screen.fill(WHITE)
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (SCREEN_SIZE[0], i * CELL_SIZE))
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_SIZE[1]))

def draw_piece(screen, row, col, color):
    pygame.draw.circle(screen, color, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)

def send_data(connection, data):
    connection.send(pickle.dumps(data))

def receive_data(connection):
    return pickle.loads(connection.recv(1024))

def chat_window(client_socket):
    def on_send():
        message = entry.get()
        if message:
            send_data(client_socket, {"message": message})
            text_box.insert(tk.END, "You: " + message + "\n")
            entry.delete(0, tk.END)

    def receive_message():
        while True:
            data = receive_data(client_socket)
            if "message" in data:
                message = data["message"]
                text_box.insert(tk.END, "Opponent: " + message + "\n")

    root = tk.Tk()
    root.title("Chat with Opponent")

    text_box = tk.Text(root)
    text_box.pack()

    entry = tk.Entry(root)
    entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
    entry.focus_set()

    send_button = tk.Button(root, text="Send", command=on_send)
    send_button.pack(side=tk.RIGHT)

    threading.Thread(target=receive_message, daemon=True).start()

    root.mainloop()

def main():
    # Connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 12345))
        print("Connected to server")
    except socket.error as e:
        print("Error occurred while connecting to server:", e)
        root.quit()
        return

    root = tk.Tk()
    root.title("Caro Client")

    def on_click(row, col):
        send_data(client_socket, (row, col))

    def on_chat_click():
        chat_window(client_socket)

    # Create GUI for board
    board_frame = tk.Frame(root)
    board_frame.pack()

    buttons = []
    for i in range(BOARD_SIZE):
        row_buttons = []
        for j in range(BOARD_SIZE):
            btn = tk.Button(board_frame, text="", width=2, height=1,
                            command=lambda r=i, c=j: on_click(r, c))
            btn.grid(row=i, column=j)
            row_buttons.append(btn)
        buttons.append(row_buttons)

    chat_button = tk.Button(root, text="Chat", command=on_chat_click)
    chat_button.pack()

    while True:
        data = receive_data(client_socket)
        if "board" in data:
            board = data["board"]
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if board[i][j] == 1:
                        buttons[i][j].config(bg="blue", state=tk.DISABLED)
                    elif board[i][j] == 2:
                        buttons[i][j].config(bg="black", state=tk.DISABLED)
        elif "winner" in data:
            print("Player", data["winner"], "wins!")
            root.quit()
            break

        root.update()

    client_socket.close()

if __name__ == "__main__":
    main()
