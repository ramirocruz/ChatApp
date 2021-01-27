import socket
import sys
import threading
from message import send_message
from encryption import Encryption, GenerateKey


SERV_IP = '127.0.0.1'
SERV_PORT = 5050


class Client:
    def __init__(self, s_addr, s_port, username):
        # Connecting to server
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((s_addr, s_port))
        self.username = username

    def start_server(self, ip, port):
        ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ssocket.bind((ip, port))

        ssocket.listen(5)
        # print("server ready..")
        while True:
            c, addr = ssocket.accept()

            sender_hash = int(c.recv(4096).decode())

            key = GenerateKey(self.username)

            c.send(str(key.hashkey).encode())
            key.gen_key(sender_hash)
            de = Encryption(key.finalkey)

            cipher = c.recv(4096)
            msg = de.decrypt(cipher).decode()
            type, msg = msg.decode().split(":")
            print(msg)

            if type == "file":
                filename = msg.split(">>")[1].strip()
                with open(filename, 'wb') as f:
                    while True:
                        # print('receiving data...')
                        data = de.decrypt(c.recv(1024))
                        if not data:
                            break

                        f.write(data)

            c.close()

    def print_cmds(self):
        cmds = ["SEND <username/groupname> <message>", "SEND <username/groupname> FILE <filepath>",
                "LIST: lists all active chats", "JOIN <groupname>: join or create a group",
                "CREATE <groupname>: create a group"]

        print("****** COMMANDS *******")
        for cmd in cmds:
            print(cmd)

        print("***********************\n")


    def run(self, ip, port):
        th = threading.Thread(target=self.start_server, args=(ip, port,))
        th.daemon
        th.start()

        self.print_cmds()
        while True:
            tokens = input().split()
            # print(tokens)
            cmd = tokens[0]
            if len(tokens) > 1:
                args = tokens[1:]

            # TODO: Error handling
            if cmd.lower() == 'send':
                if len(args) < 2:
                    print(f"ERROR: expected 2 or more arguments, got {len(args)}")
                else:
                    username = args[0]
                    msg = "send:" + username
                    self.client_socket.send(msg.encode())
                    reply = self.client_socket.recv(4096).decode()
                    ip, port = reply.split(":")
                    # print(ip, port)
                    send_message(args, ip, port)


        th.join()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        username = input()
        client = Client(SERV_IP, SERV_PORT, username)
        client.run(sys.argv[1], int(sys.argv[2]))
    else:
        print(f"ERROR: Expected 3 arguments, got {len(sys.argv)}")
        sys.exit()

