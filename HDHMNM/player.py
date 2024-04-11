class Player:
    def __init__(self, player_num, network):
        self.player_num = player_num
        self.network = network

    def select_square(self, row, col):
        # Gửi vị trí ô đã chọn tới máy chủ
        self.network.send((row, col))

    def send_message(self, message):
        # Gửi tin nhắn tới máy chủ
        self.network.send(message)

    def receive_message(self):
        # Nhận tin nhắn từ máy chủ
        return self.network.recv()

    def get_player_num(self):
        return self.player_num
