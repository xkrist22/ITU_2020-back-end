# coding=utf-8
from network_communication.client import client
from network_communication.server import server
from game_logic.ship import ship
from game_logic.user_area import user_area
import time


Server = server() # create server
ip = Server.get_ip() # get server ip


client1 = client(ip, "test") # client require ip of server and Uniqe ID
client2 = client(ip, "test2")
client3 = client(ip, "test3")

client1.send("yeet")

time.sleep(0.5) # sending takes some time

rec = client2.recive()

print(rec)
