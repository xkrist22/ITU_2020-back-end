# load additional Python modules
import socket
import time
import tkinter as tk
from tkinter import simpledialog

application_window = tk.Tk() # for simpledialog

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_hostname = socket.gethostname()
local_fqdn = socket.getfqdn()
ip_address = socket.gethostbyname(local_hostname)


ip = simpledialog.askstring(title="IP", prompt= "Enter correct server IP:",parent=application_window)

if ip is not None:

    server_address = (ip, 23456)
    sock.connect(server_address)
    print ("connecting to %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))
    data = [10, 12, 14, 15, 17]
    send = str(data).encode("utf-8")
    sock.sendall(send)
    print("sended")


sock.close()
