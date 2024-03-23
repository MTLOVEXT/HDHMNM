import pygame
import sys

# Thiết lập màn hình
WIDTH, HEIGHT = 800, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 15, 15
SQUARE_SIZE = HEIGHT // BOARD_ROWS
CIRCLE_RADIUS = SQUARE_SIZE // 2 - 5
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
def draw_board():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, (255, 255, 255), rect)
            pygame.draw.rect(win, LINE_COLOR, rect, 1)

# Vẽ quân cờ
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(win, CIRCLE_COLOR, (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2), CIRCLE_RADIUS, 2)
            elif board[row][col] == 2:
                pygame.draw.line(win, CROSS_COLOR, (col*SQUARE_SIZE + SPACE, row*SQUARE_SIZE + SQUARE_SIZE - SPACE), (col*SQUARE_SIZE + SQUARE_SIZE - SPACE, row*SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(win, CROSS_COLOR, (col*SQUARE_SIZE + SPACE, row*SQUARE_SIZE + SPACE), (col*SQUARE_SIZE + SQUARE_SIZE - SPACE, row*SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

# Đánh dấu ô được chọn
def mark_square(row, col, player):
    board[row][col] = player

# Kiểm tra chiến thắng
def check_winner(player):
    # Kiểm tra hàng
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player and board[row][col+4] == player:
                return True
    # Kiểm tra cột
    for row in range(BOARD_ROWS - 4):
        for col in range(BOARD_COLS):
            if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player and board[row+4][col] == player:
                return True
    # Kiểm tra đường chéo chính
    for row in range(BOARD_ROWS - 4):
        for col in range(BOARD_COLS - 4):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player and board[row+4][col+4] == player:
                return True
    # Kiểm tra đường chéo phụ
    for row in range(4, BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player and board[row-4][col+4] == player:
                return True
    return False

# Vẽ dấu "X" hoặc "O" tùy thuộc vào lượt của người chơi
def draw_XO(row, col):
    turn = len(history) % 2 + 1
    if row >= 0 and row <BOARD_ROWS and col >= 0 and col < BOARD_COLS and board[row][col] == 0:
        if turn == 1:
            mark_square(row, col, 1)
            history.append((row, col, 1))
        else:
            mark_square(row, col, 2)
            history.append((row, col, 2))

# Hiển thị kết quả trận đấu
def show_result(winner):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Player {winner} wins!", True, (255, 0, 0))
    
    # Tính toán kích thước của hộp thoại pop-up
    popup_width = max(text.get_width() + 40, 250)  # 40 là khoảng cách giữa văn bản và viền của hộp thoại
    popup_height = max(text.get_height() + 40, 100)  # 40 là khoảng cách giữa văn bản và viền của hộp thoại

    # Tạo hộp thoại pop-up
    popup_surface = pygame.Surface((popup_width, popup_height))
    popup_surface.fill((255, 255, 255))  # Màu nền trắng cho hộp thoại

    # Vị trí của văn bản trong hộp thoại pop-up
    text_rect = text.get_rect(center=(popup_width // 2, popup_height // 2))

    # Vẽ hộp thoại pop-up
    win.blit(popup_surface, ((WIDTH - popup_width) // 2, (HEIGHT - popup_height) // 2))
    win.blit(text, text_rect)
    pygame.display.update()

       # Đợi người chơi đóng hộp thoại
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()


# Vẽ nút Start và Exit
def draw_buttons():
    start_button = pygame.Rect(WIDTH - 150, 50, 100, 50)
    exit_button = pygame.Rect(WIDTH - 150, 150, 100, 50)

    if start_button.collidepoint(pygame.mouse.get_pos()):
        start_color = BUTTON_HOVER_COLOR
    else:
        start_color = BUTTON_COLOR
    
    if exit_button.collidepoint(pygame.mouse.get_pos()):
        exit_color = BUTTON_HOVER_COLOR
    else:
        exit_color = BUTTON_COLOR

    pygame.draw.rect(win, start_color, start_button)
    pygame.draw.rect(win, exit_color, exit_button)

    font = pygame.font.Font(None, 36)
    start_text = font.render("Start", True, TEXT_COLOR)
    exit_text = font.render("Exit", True, TEXT_COLOR)

    start_text_rect = start_text.get_rect(center=start_button.center)
    exit_text_rect = exit_text.get_rect(center=exit_button.center)

    win.blit(start_text, start_text_rect)
    win.blit(exit_text, exit_text_rect)

    return start_button, exit_button

# Kiểm tra nút được nhấn
def check_button_click(pos, start_button, exit_button):
    if start_button.collidepoint(pos):
        return True
    elif exit_button.collidepoint(pos):
        pygame.quit()
        sys.exit()
    return False

# Khởi tạo pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro")

board = create_board()
history = []
game_started = False  # Biến cờ để theo dõi xem trò chơi đã bắt đầu hay chưa

# Khai báo kích thước và vị trí của ô chat
CHAT_BOX_WIDTH = 200
CHAT_BOX_HEIGHT = 360
CHAT_BOX_X = (WIDTH - CHAT_BOX_WIDTH) // 1
CHAT_BOX_Y = HEIGHT - CHAT_BOX_HEIGHT - 0

# Màu cho border đen
BORDER_COLOR = (0, 0, 0)

# Màu chữ cho player 1 (màu đỏ)
PLAYER1_TEXT_COLOR = (255, 0, 0)

# Màu chữ cho player 2 (màu xanh)
PLAYER2_TEXT_COLOR = (0, 0, 255)

# Màu chữ mặc định cho nội dung tin nhắn
DEFAULT_TEXT_COLOR = (0, 0, 0)

# Vẽ ô chat
def draw_chat_box():
    pygame.draw.rect(win, BORDER_COLOR, (CHAT_BOX_X, CHAT_BOX_Y, CHAT_BOX_WIDTH, CHAT_BOX_HEIGHT),2)
    pygame.draw.rect(win, (255, 255, 255), (CHAT_BOX_X + 2, CHAT_BOX_Y + 2, CHAT_BOX_WIDTH - 4, CHAT_BOX_HEIGHT - 4))


# Hiển thị tin nhắn trong ô chat
def display_message(message, player, position):
    font = pygame.font.Font(None, 24)
    text_color = PLAYER1_TEXT_COLOR if player == 1 else PLAYER2_TEXT_COLOR if player == 2 else DEFAULT_TEXT_COLOR
    text = font.render(message, True, text_color)
    # Tính toán vị trí của tin nhắn dựa trên vị trí của ô chat và số thứ tự của tin nhắn
    text_x = CHAT_BOX_X + 1
    text_y = CHAT_BOX_Y + CHAT_BOX_HEIGHT - position * 20
    # Vị trí của văn bản trong ô chat
    text_rect = text.get_rect(x=text_x, y=text_y)
    win.blit(text, text_rect)



# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE
            if game_started:  # Chỉ xử lý sự kiện nhấn chuột nếu trò chơi đã bắt đầu
                draw_XO(clicked_row, clicked_col)

            # Kiểm tra nút Start và Exit
            if start_button.collidepoint((mouseX, mouseY)):
                board = create_board()
                history = []
                game_started = True
            elif exit_button.collidepoint((mouseX, mouseY)):
                pygame.quit()
                sys.exit()

    win.fill(BG_COLOR)
    draw_board()

    # Vẽ các quân cờ chỉ khi trò chơi đã bắt đầu
    if game_started:
        draw_figures()

    draw_chat_box()

    # Hiển thị tin nhắn trong ô chat
    display_message("Player 1: Hello!", player=1, position=2)
    display_message("Player 2: Hi there!", player=2, position=1)


 # Kiểm tra xem chuột có đang hover vào ô không
    mouse_pos = pygame.mouse.get_pos()
    hovered_row = mouse_pos[1] // SQUARE_SIZE
    hovered_col = mouse_pos[0] // SQUARE_SIZE
    if 0 <= hovered_row < BOARD_ROWS and 0 <= hovered_col < BOARD_COLS:
        pygame.draw.rect(win, HOVER_COLOR, (hovered_col*SQUARE_SIZE, hovered_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Vẽ nút Start và Exit
    start_button, exit_button = draw_buttons()

    # Kiểm tra chiến thắng
    if game_started and (check_winner(1) or check_winner(2)):
        show_result(1 if check_winner(1) else 2)
        game_started = False  # Đặt biến cờ game_started thành False sau khi kết thúc trò chơi

    pygame.display.update()

