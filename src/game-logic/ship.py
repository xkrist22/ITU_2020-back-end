"""
    Modul contains class for creating and working with ships
"""
__author__ = "Jiří Křištof <xkrist22@stud.fit.vutbr.cz>"
__date__ = "2020-10-12"


from copy import deepcopy


class ship:
    unknown_cell = 0
    ship_cell = 1
    max_width = 5
    max_height = 3


    def __init__(self, width: int, height: int):
        """
            Constructor of the ship

            :param width: width of the area for creating ship
            :param height: height of the area for creating ship
        """
        
        if (width > ship.max_width):
            raise ValueError("Max width of the ship is 5")
        if (height > ship.max_height):
            raise ValueError("Max height of the ship is 3")
        self.__width = width
        self.__height = height
        self.__ship_array = [ship.unknown_cell] * (width * height)


    def __len__(self) -> int:
        """
            Method returns size of the ship list

            :return: returns size of the list, which can be used to create ship
        """
        return len(self.get_ship())


    def get_ship(self) -> list:
        """
            Method returns ship list

            :return: returns list containing ship
        """
        return self.__ship_array


    def is_valid_coordinates(self, x: int, y: int) -> bool:
        """
            Method for checking coordinates – coordinates should be
            in bounds of the game area

            :param x: x-part of the coordinate
            :param y: y-part of the coordinate
            :return: return True if coordinates are in game area, else return false
        """
        if (x > self.get_width() - 1 or y > self.get_height() - 1 or x < 0 or y < 0):
            return False
        else:
            return True
        

    def get_width(self) -> int:
        """
            Getter of the width

            :return: returns width of game area
        """

        return self.__width


    def get_height(self) -> int:
        """
            Getter of the height

            :return: returns height of game area
        """

        return self.__height


    def get_cell_index(self, x: int, y: int) -> int:
        """
            Method for geting index of the cell. Cell is defined by
            coordinates, index is 1D index of list. 

            :param x: x-part of the coordinate
            :param y: y-part of the coordinate
            :return: returns 1D index into the game area             
        """
        return (self.get_width() * y) + x


    def place_ship_cell(self, *coordinates: tuple):
        """
            Method for inserting ship cells into ship area

            :param *coordinates: Tuples containing coordinates which will create ship 
        """
        for x, y in coordinates:
            if (not self.is_valid_coordinates(x, y)):
                raise IndexError("Coordinate out of ship area")
            self.get_ship()[self.get_cell_index(x, y)] = ship.ship_cell


    def place_unknown_cell(self, x: int, y: int):
        """
            Method for inserting water cell into ship area

            :param x: x-part of the coordinate
            :param y: y-part of the coordinate
        """
        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of ship area")
        self.get_ship()[self.get_cell_index(x, y)] = ship.unknown_cell


    def is_cell_ship(self, x: int, y: int) -> bool:
        """
            Method for detrmining if there is ship on the given cell
            or not

            :param x: x-part of the coordinate
            :param y: y-part of the coordinate
            :return: returns True, if cell contain ship, else return False
        """
        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of ship area")
        if (self.get_ship()[self.get_cell_index(x, y)] == ship.ship_cell):
            return True
        else:
            return False


    def remove_ship(self, x: int, y: int):
        """
            Method for removing ship from game area. Method use flood-fill

            :param x: x-coordinate of one cell where ship is
            :param y: y-coordinate of one cell where ship is
        """

        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of game area")
        if (self.get_ship()[self.get_cell_index(x, y)] != ship.ship_cell):
            raise ValueError("Cell does not contain ship")

        self.get_ship()[self.get_cell_index(x, y)] = ship.unknown_cell

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



    def is_ship_continuous(self) -> bool:
        temp_ship = deepcopy(self)
        break_outer_cycle = False
        for temp_height in range(0, temp_ship.get_height()):
            for temp_width in range(0, temp_ship.get_width()):
                if (temp_ship.is_cell_ship(temp_width, temp_height)):
                    temp_ship.remove_ship(temp_width, temp_height)
                    break_outer_cycle = True
                    break
            if (break_outer_cycle):
                break
        if (ship.ship_cell in temp_ship.get_ship()):
            return False
        else:
            return True 