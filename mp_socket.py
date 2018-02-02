import socket


class SocketClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
        self.sk.connect((self.host, self.port))  # 要连接的IP与端口

    def send_cmd(self, command):
        self.sk.send(command.encode())

    def __del__(self):
        self.sk.close()



