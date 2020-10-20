
from client import client
from server import server
import time



Server = server() # create server
ip = Server.get_ip()

client1 = client(ip, "test")
client2 = client(ip, "test2")
client3 = client(ip, "test3")


client1.send("test!")
client2.send("test@@")

time.sleep(0.4)

print(client3.recive())
