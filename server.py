import socket
import threading
import sys

class Server:
    IP = socket.gethostbyname(socket.gethostname())
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.connections = []

    def handle_connection(self,client_socket,client_address):
        while True:
            data = client_socket.recv(4096)
            msg = "< {} : {} > :~ ".format(client_address[0],client_address[1]) + data.decode()
            for client in self.connections:
                if(client != client_socket):
                    client.send(msg.encode())
            if not data:
                print("{}:{} disconnected.....".format(client_address[0],client_address[1]))
                self.connections.remove(client_socket)
                client_socket.close()
                break

    def run(self,PORT=18000):
        self.server_socket.bind((self.IP,PORT))
        self.server_socket.listen(1)
        print("Listening at {}".format(self.server_socket.getsockname()))
        while True:
            client_socket,client_address = self.server_socket.accept()
            print("{}:{} connected.....".format(client_address[0],client_address[1]))
            self.connections.append(client_socket)
            th = threading.Thread(target=self.handle_connection,args=(client_socket,client_address))
            th.daemon = True
            th.start()

if __name__ == "__main__":
    server = Server()
    if(len(sys.argv)==1):
        server.run()
    else:
        server.run(int(sys.argv[1]))
        