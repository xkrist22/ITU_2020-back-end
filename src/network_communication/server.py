import socket
import threading

class server:

    def __init__(self, port=None):
        if port is not None:
            self.port = port
        else:
            self.port = 30000
        self.ip = socket.gethostbyname(socket.gethostname())
        threading.Thread(target=self.start_server,args=(self.ip,)).start()

    def start_server(self, ip):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clients = []
        self.s.bind((ip ,self.port))
        self.s.listen(100)
        self.username_lookup = {}
        print("server OK ")

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            self.username_lookup[c] = username
            self.clients.append(c)
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self,msg):
        for connection in self.clients:
            connection.send(msg.encode())
    def get_ip(self):
        return self.ip

    def handle_client(self,c,addr):
        while True:
            try:
                msg = c.recv(1024)
            except:
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)
                self.broadcast(str(self.username_lookup[c])+' has left the room.')
                break

            if msg.decode() != '':
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)
