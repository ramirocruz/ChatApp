import socket
import sys
import threading
import time



class Client:
    def __init__(self,server_ip,server_port, sip,sport):
        self.client_socket =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((server_ip,server_port))
        self.sip=sip
        self.sport=sport
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.text=''
        self.user_name=''
        # self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    def senddata(self):
        self.client_socket.send((self.sip+':'+str(self.sport)).encode())
        while True:
            inp=input()
            tokens=inp.split()
            if tokens[0]=='send':
                # if tokens[1]!='file':
                self.client_socket.send((tokens[0]+' '+tokens[1]).encode())
                self.text=inp.split(' ',2)[2]
                # else:
                #     self.client_socket.send((tokens[0]+' '+tokens[2]).encode())
                    # self.text=inp.split(' ',2)[2]
            elif tokens[0]=='send_file':
                pass            
            elif tokens[0]=='group_send':
                self.client_socket.send((tokens[0]+' '+tokens[1]).encode())
                self.text=inp.split(' ',2)[2]
            elif tokens[0]=='login':
                self.user_name=tokens[1]
                self.client_socket.send(inp.encode())
            else:
                self.client_socket.send(inp.encode())

    def handle_connection(self,client_socket,client_address):
        while True:
            data=client_socket.recv(4096)
            if not data:
                break
            print(data.decode())
            

    def server(self):
        self.server_socket.bind((self.sip,self.sport))
        self.server_socket.listen(20)
        print("Listening at {}".format(self.server_socket.getsockname()))
        while True:
            client_socket,client_address=self.server_socket.accept()
            # print(client_address[0],client_address[1],' connected')
            th=threading.Thread(target=self.handle_connection,args=(client_socket,client_address))
            th.daemon = True
            th.start()

    def run(self):
        th1 = threading.Thread(target=self.senddata)
        th1.daemon=True
        th1.start()
        th2=threading.Thread(target=self.server)
        th2.daemon=True
        th2.start()
        while True:
            data = self.client_socket.recv(4096)
            if not data:
                break
            if data.decode()[:4].lower()=='send':
                ip,port=data.decode()[5:].split(':')
                p2psocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                p2psocket.connect((ip,int(port)))
                p2psocket.send((self.user_name+' : '+self.text).encode())
                p2psocket.close()
                # print(ip)
                # print(port)
                # print(message)
            elif data.decode()[:10].lower()=='group_send':
                data=data.decode()[11:]
                members=data.split(';')[:-1]
                groupname=data.split(';')[-1]
                for i in members:
                    ip,port=i.split(':')
                    p2psocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    p2psocket.connect((ip,int(port)))
                    p2psocket.send((self.user_name+' '+groupname+' : '+self.text).encode())
                    p2psocket.close()
            elif data.decode()[:4].lower()=='list_groups':
                print(data.decode()[5:])
            else:
                print(data.decode())


if __name__ == "__main__":
    client = Client(sys.argv[1],int(sys.argv[2]),sys.argv[3],int(sys.argv[4]))
    client.run()