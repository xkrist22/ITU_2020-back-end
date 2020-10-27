# coding=utf-8
from network_communication.client import client
from network_communication.server import server
from game_logic.ship import ship
from game_logic.user_area import user_area
from game_logic.enemy_area import enemy_area
import time
import json

class player:

    def __init__(self, username: str, ip: int):
        """
            Constructor for creating player
        """

        self.__username = username
        self.__ip = ip
        self.__client = client(ip, None, username)
        self.__unread_messages = []
        self.__own_area = user_area(10, 10)
        self.__enemy_area = enemy_area(10, 10)


    def get_username(self) -> str:
        return self.__username
    
    def get_ip(self) -> int:
        return self.__ip
    
    def get_client(self) -> client:
        return self.__client
    
    def get_unread_messages(self):
        return self.__unread_messages
    
    def get_pop_message(self) -> str:
        return self.__unread_messages.pop(0)
    
    def get_own_area(self):
        return self.__own_area

    def get_enemy_area(self):
        return self.__enemy_area

    def send_plain_message(self, message: str):
        self.get_client().send(message)
    
    def send_structured_message(self, action: str, data: dict):
        obj = {"player": self.get_username(), "action": action, **data}
        mes = json.dumps(obj)
        self.get_client().send(mes)
    
    def recieve_messages(self):
        unread = self.get_unread_messages()
        unread += self.get_client().recive()
    
    def shoot(self, x: int, y: int):
        if(self.get_enemy_area().can_shoot(x, y)):
            self.send_structured_message("shoot", {"x": x, "y": y})
    
    def register_hit(self, x: int, y: int):
        self.get_own_area().shoot(x, y)
    