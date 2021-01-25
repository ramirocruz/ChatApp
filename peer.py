import socket
import sys
import threading
from message import send_message


SERV_IP = '127.0.0.1'
SERV_PORT = 5050


class Client:
    def __init__(self, s_addr, s_port):
        # Connecting to server
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((s_addr, s_port))

    def start_server(self, ip, port):
        ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ssocket.bind((ip, port))

        ssocket.listen(5)
        # print("server ready..")
        while True:
            c, addr = ssocket.accept()
            c.send("Success".encode())

            msg = c.recv(4096)
            msg = msg.decode()
            print(msg)

            c.close()

    def run(self, ip, port):
        th = threading.Thread(target=self.start_server, args=(ip, port,))
        th.daemon
        th.start()

        while True:
            tokens = input().split()
            # print(tokens)
            cmd = tokens[0]
            if len(tokens) > 1:
                args = tokens[1:]

            # TODO: Error handling
            if cmd == 'SEND':
                if len(args) < 2:
                    print(f"ERROR: expected 2 or more arguments, got {len(args)}")
                else:
                    username = args[0]
                    msg = "send:" + username
                    self.client_socket.send(msg.encode())
                    reply = self.client_socket.recv(4096).decode()
                    ip, port = reply.split(":")
                    # print(ip, port)
                    send_message(args[1], ip, port)


        th.join()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        client = Client(SERV_IP, SERV_PORT)
        client.run(sys.argv[1], int(sys.argv[2]))
    else:
        print(f"ERROR: Expected 3 arguments, got {len(sys.argv)}")
        sys.exit()

