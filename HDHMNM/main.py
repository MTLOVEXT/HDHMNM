import pygame
import socket
import pickle

# Thiết lập màn hình
WIDTH, HEIGHT = 800, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 15, 15
CELL_SIZE = HEIGHT // BOARD_ROWS
CIRCLE_RADIUS = CELL_SIZE // 2 - 5
CROSS_WIDTH = 5
SPACE = 30
# Colors
BG_COLOR = (255, 255, 255)  # Đổi màu nền thành màu trắng
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (255, 0, 0)
CROSS_COLOR = (0, 0, 255)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (150, 150, 150)  # Đổi màu của nút thành màu xám nhạt
BUTTON_HOVER_COLOR = (100, 100, 100)  # Đổi màu khi di chuột qua nút thành màu xám đậm

# Tạo bàn cờ
def create_board():
    board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

# Thêm màu cho ô khi hover vào
HOVER_COLOR = (242, 243, 244)
# Vẽ bảng
def draw_board(screen):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (255, 255, 255), rect)
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)

def draw_piece(screen, row, col, color):
    pygame.draw.circle(screen, color, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CIRCLE_RADIUS, 2)

def send_data(connection, data):
    connection.send(pickle.dumps(data))

def receive_data(connection):
    return pickle.loads(connection.recv(1024))

def main():
    # Connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 12345))
        print("Connected to server")
    except socket.error as e:
        print("Error occurred while connecting to server:", e)
        return

    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Caro")

    board = create_board()
    history = []
    game_started = False  

    CHAT_BOX_WIDTH = 200
    CHAT_BOX_HEIGHT = 360
    CHAT_BOX_X = (WIDTH - CHAT_BOX_WIDTH) // 1
    CHAT_BOX_Y = HEIGHT - CHAT_BOX_HEIGHT - 0

    BORDER_COLOR = (0, 0, 0)
    PLAYER1_TEXT_COLOR = (255, 0, 0)
    PLAYER2_TEXT_COLOR = (0, 0, 255)
    DEFAULT_TEXT_COLOR = (0, 0, 0)

    def draw_chat_box():
        pygame.draw.rect(win, BORDER_COLOR, (CHAT_BOX_X, CHAT_BOX_Y, CHAT_BOX_WIDTH, CHAT_BOX_HEIGHT), 2)
        pygame.draw.rect(win, (255, 255, 255), (CHAT_BOX_X + 2, CHAT_BOX_Y + 2, CHAT_BOX_WIDTH - 4, CHAT_BOX_HEIGHT - 4))

    def display_message(message, player, position):
        font = pygame.font.Font(None, 24)
        text_color = PLAYER1_TEXT_COLOR if player == 1 else PLAYER2_TEXT_COLOR if player == 2 else DEFAULT_TEXT_COLOR
        text = font.render(message, True, text_color)
        text_x = CHAT_BOX_X + 1
        text_y = CHAT_BOX_Y + CHAT_BOX_HEIGHT - position * 20
        text_rect = text.get_rect(x=text_x, y=text_y)
        win.blit(text, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                client_socket.close()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = mouseY // CELL_SIZE
                clicked_col = mouseX // CELL_SIZE
                if game_started:  
                    draw_piece(win, clicked_row, clicked_col, CIRCLE_COLOR)
                    send_data(client_socket, (clicked_row, clicked_col))

        win.fill(BG_COLOR)
        draw_board(win)
        draw_chat_box()

        # Hiển thị tin nhắn trong ô chat
        display_message("Player 1: Hello!", player=1, position=2)
        display_message("Player 2: Hi there!", player=2, position=1)

        pygame.display.update()

if __name__ == "__main__":
    main()
