import socket
import threading

class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.clientEcho,args = (client,address)).start()

    def clientEcho(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    response = (data + ": Recieved, Thank You for choosing this python server for your echo needs. Please come back soon!")
                    client.send(response)
                    print data
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    while True:
        port_num = 10000
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    Server('',port_num).listen()