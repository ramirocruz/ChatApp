import socket
import threading
import sys

peer_info = {'peer1':['127.0.0.1', '5051'], 'peer2':['127.0.0.1', '5052']}


class Server:
    # IP = socket.gethostbyname(socket.gethostname())
    IP = '127.0.0.1'

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.connections = []

    def handle_connection(self, client_socket, client_address):
        while True:
            data = client_socket.recv(4096)
            tokens = data.decode().split(":")
            # TODO: Error handling
            if tokens[0] == "send":
                pip, pport = peer_info[tokens[1]]
                msg = f"{pip}:{pport}".encode()
                client_socket.send(msg)

            # msg = "{}:{}:~ ".format(client_address[0], client_address[1]) + data.decode()
            # print("sending..",msg)
            # for client in self.connections:
            #     if client != client_socket:
            #         client.send(msg.encode())

            if not data:
                print("{}:{} disconnected.....".format(client_address[0], client_address[1]))
                self.connections.remove(client_socket)
                client_socket.close()
                break

    def run(self, port=18000):
        self.server_socket.bind((self.IP, port))
        self.server_socket.listen(1)
        print("Listening at {}".format(self.server_socket.getsockname()))
        while True:
            client_socket, client_address = self.server_socket.accept()
            print("{}:{} connected.....".format(client_address[0], client_address[1]))
            self.connections.append(client_socket)
            th = threading.Thread(target=self.handle_connection,args=(client_socket, client_address))
            th.daemon = True
            th.start()


if __name__ == "__main__":
    server = Server()
    if len(sys.argv) == 1:
        server.run()
    else:
        server.run(int(sys.argv[1]))
