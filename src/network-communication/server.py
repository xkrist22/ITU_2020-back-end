import socket
import threading


class network:
    def __init__(self, ip=None, username = None):
        if ip is None:
            self.ip = socket.gethostbyname(socket.gethostname())
            # if no ip is provided start server on local pc
            # start new thread with server on it...
            threading.Thread(target=self.start_server,args=(self.ip,)).start()

        else:
            self.ip = ip
            if username is None:
                self.username = "CLIENT 1"
            else:
                self.username = username
            print("running host on ip", ip)
            self.create_connection()
    def get_ip(self):
        return self.ip

######################## SERVER SIDE ####################################
    def start_server(self, ip):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clients = []
        self.s.bind((ip ,30000))
        self.s.listen(100)
        self.username_lookup = {}

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            self.broadcast('New person joined the room. Username: '+username)
            self.username_lookup[c] = username
            self.clients.append(c)
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self,msg):
        for connection in self.clients:
            connection.send(msg.encode())

    def handle_client(self, c, addr):
        self.last_message = ""
        while True:
            try:
                msg = c.recv(1024)
            except:
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)
                print(str(self.username_lookup[c])+' left the room.')
                self.broadcast(str(self.username_lookup[c])+' has left the room.')

                break

            if msg.decode() != '':
                #print(str(msg.decode()))
                self.last_message = str(msg.decode())
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)
    def recive(self):
        return self.last_message

##############################################################################



###################### CLIENT SIDE ###########################################
    def create_connection(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        while 1:
            try:
                print(self.ip)
                self.s.connect((self.ip ,30000))
                break
            except:
                print("Couldn't connect to server")

        self.s.send(self.username.encode())

        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler,args=())
        input_handler.start()

    def handle_messages(self):
        while 1:
            print(self.s.recv(1204).decode())

    def input_handler(self):
        while 1:
            self.s.send((self.username+' - '+input()).encode())

    def send(self, message):
        self.s.send((message).encode())


#############################################################################
