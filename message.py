import socket
import sys
from threading import Thread

SERV_IP = '127.0.0.1'
SERV_PORT = 5050


def send_message(args, ip, port):
    # print("sending..", args[1])
    psocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    psocket.connect((ip, int(port)))
    reply = psocket.recv(4096)
    username = args[0]
    # TODO: Add encryption
    if args[1].lower() == 'file':
        filepath = args[2]
        filename = filepath.split('\\')[-1]
        msg = f"file:{username} >> {filename}"
        psocket.send(msg.encode())

        try:
             with open(filepath, 'rb') as f:
                l = f.read(4096)
                while(l):
                    psocket.send(l)
                    l = f.read(4096)

        except FileNotFoundError as e:
            print("ERROR:", e)
            print("\n\n")
    else:
        msg = f"message:{username} >> {args[1]}"
        psocket.send(msg.encode())

    psocket.close()
    return


def start_server(ip, port):
    ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ssocket.bind((ip, port))

    ssocket.listen(5)

    while True:
        c, addr = ssocket.accept()
        c.send("Success".encode())

        msg = c.recv(1024)
        msg = msg.decode()
        print(msg)

        c.close()


if __name__ == "__main__":
    l_ip = str(sys.argv[1])
    l_port = int(sys.argv[2])

    thread = Thread(target=start_server, args=(l_ip, l_port,))
    thread.start()

    psocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    psocket.connect((SERV_IP, SERV_PORT))

    psocket.recv(1024)
    send_msg = input()
    psocket.send(send_msg.encode())

    msg = psocket.recv(1024)
    msg = msg.decode()
    print(msg)
    p_ip, p_port = msg.split()
    psocket.close()

    send_msg = input()
    psocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    psocket.connect((p_ip, int(p_port)))
    psocket.recv(1024)

    psocket.send(send_msg.encode())
    psocket.close()

    thread.join()
