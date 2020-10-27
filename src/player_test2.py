# coding=utf-8
from network_communication.client import client
from network_communication.server import server
from game_logic.ship import ship
from game_logic.user_area import user_area
from player import player
import time
import json

ip = "127.0.1.1"
#ip = "192.168.0.1"

player1 = player("username2", ip)

player1.send_plain_message("message2")

time.sleep(1)

#build ships

ships = []
ships.append( ship(3, 2) )
ships.append( ship(1, 1) )
ships.append( ship(5, 2) )

ships[0].place_ship_cell((0,0), (1,0), (2,0), (1,1))
ships[1].place_ship_cell((0,0))
ships[2].place_ship_cell((0,0), (1,0), (2,0), (3,0), (4,0), (1,1), (3,1))

player1.get_own_area().place_ship(0, 0, ships[0])
player1.get_own_area().place_ship(9, 0, ships[1])
player1.get_own_area().place_ship(4, 4, ships[2])

#game time

shoot_targets = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(3,4),(4,4),(5,4),(4,5),(9,9)]

for x,y in shoot_targets:
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