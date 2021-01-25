import socket
import sys
import threading
from message import send_message


class Client:
    def __init__(self, addr, port=18000):
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((addr, port))

    def send_data(self):
        while True:
            tokens = input().split()
            # print(tokens)
            cmd = tokens[0]
            if len(tokens) > 1:
                args = tokens[1:]

            if cmd == 'SEND':
                if len(args) < 2:
                    print(f"ERROR: expected 2 or more arguments, got {len(args)}")
                else:
                    send_message(self.client_socket, args)
            # self.client_socket.send()

    def run(self):
        th = threading.Thread(target=self.send_data)
        th.daemon
        th.start()
        while True:
            data = self.client_socket.recv(4096)
            if not data:
                break
            print(data.decode())


if __name__ == "__main__":
    if len(sys.argv) == 2:
        client = Client(sys.argv[1])
    elif len(sys.argv) > 2:
        client = Client(sys.argv[1],int(sys.argv[2]))
    else:
        print(f"ERROR: Expected 2 or 3 arguments, got {len(sys.argv)}")
        sys.exit()

    client.run()