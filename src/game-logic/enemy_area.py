import random


class enemy_area:
    unknown_cell = 0
    shooted_ship_cell = 2
    shooted_empty_cell = 3


    def __init__(self, width: int, height: int):
        """
            Constructor of the ship

            :param width: width of the area for creating ship
            :param height: height of the area for creating ship
        """

        self.__x = width
        self.__y = height
        self.__area = [enemy_area.unknown_cell] * (width * height)


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


    def is_shooted_cell(self, x: int, y: int) -> bool:
        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of game area")
        if (self.get_area()[self.get_cell_index(x, y)] == enemy_area.shooted_empty_cell or self.get_area()[self.get_cell_index(x, y)] == enemy_area.shooted_ship_cell):
            return True
        else:
            return False


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


    # method for simulated shooting
    # should be replaced by network communication
    def shooting_stub(self) -> bool:
        if (random.randint(0, 100) % 2 == 0):
            return True
        else:
            return False 


    def shoot(self, x: int, y: int) -> bool:
        """
            Method simulating shooting into the enemy game area
            Method is called when app sends "shoot info" to the second player

            :param x: x-part of the coordinate
            :param y: y-part of the coordinate
            :return: returns True if ship was shooted, else returns False
        """

        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of game area")
        if (self.is_shooted_cell(x, y)):
            raise ValueError("Cell is already shooted")
        
        #TODO network communication – is selected cell ship, or water
        is_ship = self.shooting_stub() # this info should be extracted from network communication

        if (is_ship):
            self.get_area()[self.get_cell_index(x, y)] = enemy_area.shooted_ship_cell
            return True
        else:
            self.get_area()[self.get_cell_index(x, y)] = enemy_area.shooted_empty_cell
            return False


    def shoot_bomb(self, x: int, y: int) -> bool:
        """
            Method simulating shooting bomb into the enemy game area
            Method is called when app sends "shoot bomb info" to the second player
            bomb causes shooting over 3x3 array

            :param x: x-part of the center of the shooted grid
            :param y: y-part of the center of the shooted grid
            :return: returns True if at least one cell ship was shooted, else returns False
        """

        grid = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        is_shooted_grid = []
        for x_c, y_c in grid:
            is_shooted_grid.append(self.shoot(x_c, y_c))
        if(any(is_shooted_grid)):
            return True
        else:
            return False
