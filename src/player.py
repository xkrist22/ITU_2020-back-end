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
            Constructor of player

            :param username: Username of player
            :param ip: IP of server player wants to join
        """

        self.__username = username
        self.__ip = ip
        self.__client = client(ip, None, username)
        self.__unread_messages = []
        self.__own_area = user_area(10, 10)
        self.__enemy_area = enemy_area(10, 10)


    def get_username(self) -> str:
        """
            Getter of username

            :return: Returns username (type str)
        """
        return self.__username
    
    def get_ip(self) -> int:
        """
            Getter of ip

            :return: Returns IP (type int)
        """
        return self.__ip
    
    def get_client(self) -> client:
        """
            Getter of client

            :return: Returns clien (type client)
        """
        return self.__client
    
    def get_unread_messages(self) -> list:
        """
            Getter of unread messages

            :return: Returns unread messages (type list)
        """
        return self.__unread_messages
    
    def get_pop_message(self) -> str:
        """
            Removes message from unread_messages, returns it

            :return: Returns oldest unprocessed message (type str)
        """
        return self.__unread_messages.pop(0)
    
    def get_own_area(self) -> user_area:
        """
            Getter of player_area object

            :return: Returns own_area (type user_area)
        """
        return self.__own_area

    def get_enemy_area(self) -> enemy_area:
        """
            Getter of enemy_area object

            :return: Returns enemy_area (type enemy_area)
        """
        return self.__enemy_area

    def send_plain_message(self, message: str):
        """
            Sends string to server
        """
        self.get_client().send(message)
    
    def send_structured_message(self, action: str, data: dict):
        """
            Sends JSON to server

            Structure of JSON:
            player: sender's name
            action: type of message (shoot, message, ...)
            other keys: data for action (for example coordinates of shooting)
        """

        obj = {"player": self.get_username(), "action": action, **data}
        mes = json.dumps(obj)
        self.get_client().send(mes)
    
    def recieve_messages(self):
        """
            Appends unread_messages with new messages from server
        """
        unread = self.get_unread_messages()
        unread += self.get_client().recive()
    
    def shoot(self, x: int, y: int):
        """
            Checks if coordinates are in range and sends shoot message to the server
        """
        if(self.get_enemy_area().can_shoot(x, y)):
            self.send_structured_message("shoot", {"x": x, "y": y})
    
    def register_hit(self, x: int, y: int):
        """
            Marks enemy's shot to your field
        """
        self.get_own_area().shoot(x, y)
    