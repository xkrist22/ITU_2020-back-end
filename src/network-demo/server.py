import socket
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog, Text
from functools import partial
from tkinter import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_hostname = socket.gethostname()
local_fqdn = socket.getfqdn()
port = 23456
server_address = (socket.gethostbyname(local_hostname) , 23456) # start server on same IP as PC


class connection():

    def connect():
        while True:
            # wait for a connection
            print ('waiting for a connection on port: ', port)
            connection, client_address = sock.accept()

            try:
                # show who connected to us
                print ('connection from', client_address)

                # receive the data in small chunks and print it
                while True:
                    data = connection.recv(64)
                    if data:
                        # output received data
                        print ("Data: %s" % data)

                    else:
                        # no more data -- quit the loop
                        print ("no more data.")
                        break
            finally:
                # Clean up the connection
                connection.close()


    def start_server():

        print ('starting up on %s port %s' % server_address)
        sock.bind(server_address)
        sock.listen(1)
        connection.connect()




class Gui():
    root = tk.Tk()
    canvas = tk.Canvas(root, height = 480, width = 240, bg = "Grey")
    canvas.pack()

    frame1 = tk.Frame(root, bg = "black") #start
    frame1.place(relwidth = 0.9, relheight = 0.05, relx = 0.02, rely = 0.05)
    frame2 = tk.Frame(root, bg = "black") #stop
    frame2.place(relwidth = 0.9, relheight = 0.05, relx = 0.02, rely = 0.12)



    start = tk.Button(frame1, text = "Start server", fg = "black", bg = "green", padx=100,pady=25, command=partial(connection.start_server)) #start
    start.pack()
    stop = tk.Button(frame2, text = "Stop server", fg = "black", bg = "red", padx=100,pady=25) #stop
    stop.pack()

    #c1 = tk.Checkbutton(root, text='Restore Weights',command=var1, onvalue=1, offvalue=0).place(x=40, y=240)
    root.mainloop()
