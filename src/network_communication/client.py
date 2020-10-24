import socket
import threading


class client:
    def __init__(self, ip = None, port = None, username = None):
        if port is not None:
            self.port = port
        else:
            self.port = 30000

        self.ip = ip
        self.username = username
        if port is not None:
            self.port = port

        self.create_connection()

        self.last_message = []
        self.port = 30000


    def create_connection(self):
        print("Client OK")
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        while 1:
            try:
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
            msg = self.s.recv(1204).decode()
            if msg != '':
                if msg not in self.last_message:
                    self.last_message.append(msg)

    def input_handler(self):
        while 1:
            self.s.send((input()).encode())
    def send(self, message):
        self.s.send(message.encode())

    def recive(self):
        to_send = self.last_message
        self.last_message=[]
        return to_send

    def exit(self):
        print("shuting down client\n")
        self.s.shutdown(socket.SHUT_RDWR)
        print("bye...")
