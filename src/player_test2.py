# coding=utf-8
from network_communication.client import client
from network_communication.server import server
from game_logic.ship import ship
from game_logic.user_area import user_area
from player import player
import time
import json


Server = server() # create server
ip = Server.get_ip() # get server ip

player1 = player("username2", ip)

player1.send_message("message2")

time.sleep(1)

#build ships


#game time

shoot_targets = [(7,0),(7,1),(7,2),(8,3),(8,4),(8,5)]

for i in range(0, 6):
    x, y = shoot_targets[i]
    print("Shooting ",x, "/", y)
    player1.shoot(x, y)
    while True:
        player1.recieve_messages()
        if player1.get_unread_messages():
            message = player1.get_pop_message()
            try:
                obj = json.loads(message)
                print(obj)
                action = obj["action"]
            except KeyError:
                print("Message does not contain action. Message classified as chat")
                action = "chat"
            except ValueError:
                print( 'Decoding JSON has failed')
                action = "chat"
            
            if action == "shoot":
                try:
                    hit_x = obj["x"]
                    hit_y = obj["y"]
                    player1.register_hit(hit_x, hit_y)
                    print("registered hit")
                except KeyError:
                    print("Message does not contain coordinates")
                except IndexError:
                    print("Enemy tried to shoot out of bounds")
            
            if action == "chat":
                print("Recieved message: ", message)
            
            break

print("end")