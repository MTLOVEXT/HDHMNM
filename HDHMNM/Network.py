import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.12"
        self.port = 3306
        self.addr = (self.server, self.port)
        self.pos = None
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.pos = self.recv_pos()
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def recv(self):
        try:
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def recv_pos(self):
        try:
            self.client.send(pickle.dumps("get_pos"))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
