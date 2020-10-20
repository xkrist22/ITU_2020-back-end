
from client import client
from server import server
import time



Server = server() # create server
ip = Server.get_ip() # get server ip



client1 = client(ip, "test") # client require ip of server and Uniqe ID
client2 = client(ip, "test2")
client3 = client(ip, "test3")

print("__________________________________")
client1.send("test!")   # broadcast message to other clients
client2.send("test@@")


time.sleep(0.5) # some delay in communication

# messages are stored in list
# calling client.recive() will sent list of messages to output and free stored messages
list = []
list.append("test!")

if list == client2.recive():
    print("List only contain messages from other clients\n")


list.append("test@@")

if list == client3.recive():
    print("Client.recive contain all unread brodcasted messages...")
    print("succes")
