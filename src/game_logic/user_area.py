# coding=utf-8
"""
    Modul contains class for working with player game area. 
"""
__author__ = "Jiří Křištof <xkrist22@stud.fit.vutbr.cz>"
__date__ = "2020-10-12"



from . import ship

class user_area:
    """
        Class containing methods for working with player game area and
        class variables used as markers of the game area.s
    """
    
    unknown_cell = 0
    ship_cell = 1
    shooted_ship_cell = 2
    shooted_empty_cell = 3


    def __init__(self, width: int, height: int):
        """
            Constructor for creating player game area

            :param width: width of the game area
            :param height: height of the game area
            :return: returns nothing
        """

        self.__x = width
        self.__y = height
        self.__area = [user_area.unknown_cell] * (width * height)


    def get_area(self) -> list:
        """
            Getter of the game area
            
            :return: returns game area list
        """

        return self.__area


    def is_valid_coordinates(self, x: int, y: int) -> bool:
        """
            Method for checking coordinates – coordinates should be
            in bounds of the game area

            :param x: x-part of the coordinate
            :param y: y-part of the coordinate
            :return: return True if coordinates are in game area, else return false
        """

        if (x > self.get_x() - 1 or y > self.get_y() - 1 or x < 0 or y < 0):
            return False
        else:
            return True
        

    def get_x(self) -> int:
        """
            Getter of the width

            :return: returns width of game area
        """

        return self.__x


    def get_y(self) -> int:
        """
            Getter of the height

            :return: returns height of game area
        """

        return self.__y


    def get_cell_index(self, x: int, y: int) -> int:
        """
            Method for geting index of the cell. Cell is defined by
            coordinates, index is 1D index of list. 

            :param x: x-part of the coordinate
            :param y: y-part of the coordinate
            :return: returns 1D index into the game area             
        """

        return (self.get_x() * y) + x


    def place_ship(self, x: int, y: int, s: ship):
        """
            Method for inserting ship into game area

            :param x: x-part of the starting coordinate
            :param y: y-part of the starting coordinate
            :param s: instance of the ship which will be inserted into game area
        """

        if (not self.is_valid_coordinates(x, y) or not self.is_valid_coordinates(x + s.get_width() - 1, y + s.get_height() - 1)):
            raise IndexError("Coordinate out of game area")
        
        height = s.get_height() 
        while height:
            width = s.get_width()
            while width:
                self.get_area()[self.get_cell_index(x + width - 1, y + height - 1)] = s.get_ship()[s.get_cell_index(width - 1, height - 1)]
                width = width - 1
            height = height - 1


    def remove_ship(self, x: int, y: int):
        """
            Method for removing ship from game area. Method use flood-fill

            :param x: x-coordinate of one cell where ship is
            :param y: y-coordinate of one cell where ship is
        """
    
        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of game area")
        if (self.get_area()[self.get_cell_index(x, y)] != user_area.ship_cell):
            raise ValueError("Cell does not contain ship")

        self.get_area()[self.get_cell_index(x, y)] = user_area.unknown_cell

        try:
            self.remove_ship(x + 1, y)
        except (ValueError, IndexError):
            pass

        try:
            self.remove_ship(x - 1, y)
        except (ValueError, IndexError):
            pass

        try:
            self.remove_ship(x, y + 1)
        except (ValueError, IndexError):
            pass

        try:
            self.remove_ship(x, y - 1)
        except (ValueError, IndexError):
            pass

   
    def place_unknown_cell(self, x: int, y: int):
        """
            Method for inserting unknown cell (means water) into the game area
            
            :param x: x-part of the coordinate
            :param y: y-part of the coordinate
        """

        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of game area")
        self.get_area()[self.get_cell_index(x, y)] = user_area.unknown_cell


    def is_cell_ship(self, x: int, y: int) -> bool:
        """
            Method for detrmining if there is ship on the given cell
            or not

            :param x: x-part of the coordinate
            :param y: y-part of the coordinate
            :return: returns True, if cell contain ship, else return False
        """

        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of game area")
        if (self.get_area()[self.get_cell_index(x, y)] == user_area.ship_cell):
            return True
        else:
            return False


    def is_shooted_cell(self, x: int, y: int) -> bool:
        """
            Method for determining if there is shooted ship on the given vell
            or not

            :param x: x-part of the coordinate
            :param y: y-part of the coordinate
            :return: returns True, if cell contain shooted ship, else return False
        """

        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of game area")
        if (self.get_area()[self.get_cell_index(x, y)] == user_area.shooted_empty_cell or self.get_area()[self.get_cell_index(x, y)] == user_area.shooted_ship_cell):
            return True
        else:
            return False


    def shoot(self, x: int, y: int) -> bool:
        """
            Method simulating shooting into the player game area
            Method is called when app get "shoot info" from network

            :param x: x-part of the coordinate
            :param y: y-part of the coordinate
            :return: returns True if ship was shooted, else returns False
        """

        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of game area")
        if (self.is_shooted_cell(x, y)):
            raise IndexError("Coordinate out of game area")
        
        if (self.is_cell_ship(x, y)):
            self.get_area()[self.get_cell_index(x, y)] = user_area.shooted_ship_cell
            return True
        else:
            self.get_area()[self.get_cell_index(x, y)] = user_area.shooted_empty_cell
            return False


    def all_ships_shooted(self) -> bool:
        """
            Method for checking if there is at least one ship, 
            which is not shooted.

            :return: return True, if all ships are sinked, else return False
        """

        if user_area.ship_cell in self.get_area():
            return False
        else:
            return True
