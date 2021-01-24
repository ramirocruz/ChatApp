import socket
import sys
import threading

class Client:
    def __init__(self,addr,PORT=18000):
        self.client_socket =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((addr,PORT))
    def senddata(self):
        while True:
            self.client_socket.send(input().encode())
    def run(self):
        th = threading.Thread(target=self.senddata)
        th.daemon
        th.start()
        while True:
            data = self.client_socket.recv(4096)
            if not data:
                break
            print(data.decode())

if __name__ == "__main__":
    if(len(sys.argv) == 2):
        client = Client(sys.argv[1])
    elif(len(sys.argv) >2):
        client = Client(sys.argv[1],int(sys.argv[2]))

client.run()