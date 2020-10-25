"""
    Modul contains class for working with player game area. 
"""
__author__ = "Jiří Křištof <xkrist22@stud.fit.vutbr.cz>"
__date__ = "2020-10-24"


from ship import ship
from random import randint
from sys import maxsize


class user_area:
    """
        Class containing methods for working with player game area and
        class variables used as markers of the game area.s
    """
    
    unknown_cell = 0
    ship_cell = 1
    shooted_ship_cell = 2
    shooted_empty_cell = 3
    rock_cell = 4

    min_width = 6
    min_height = 6

    def __init__(self, width: int, height: int):
        """
            Constructor for creating player game area

            :param width: width of the game area
            :param height: height of the game area
            :return: returns nothing
        """
        if (width < user_area.min_width):
            raise ValueError("Width must be at least " + str(user_area.min_width) + ", not " + str(width))
        if (height < user_area.min_height):
            raise ValueError("Height must be at least " + str(user_area.min_height) + ", not " + str(height))

        self.__x = width
        self.__y = height
        self.__area = [user_area.unknown_cell] * (width * height)


    def __repr__(self):
        """
            Method printing game area in grid

            :return: Returns string representation of the game area
        """
        i = 0
        height = 0
        width = self.get_x()
        str_area = ""
        while(i < self.get_y()):
            str_area += (str(self.get_area()[height:width]) + "\n")
            height += self.get_y()
            width += self.get_x()
            i += 1
        return str_area



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
            raise IndexError("Coordinate [" + str(x) + ", " + str(y) + "] out of game area")

        if (not s.is_ship_continuous()):
            raise ValueError("Inserted ship is not continuous!")
        
        height = s.get_height() 
        while height:
            width = s.get_width()
            while width:
                if (self.get_area()[self.get_cell_index(x + width - 1, y + height - 1)] == user_area.ship_cell):
                    raise ValueError("Cell [" + str(x + width - 1) + ", " + str(y + height - 1) + "] already contains ship")
                if (self.get_area()[self.get_cell_index(x + width - 1, y + height - 1)] == user_area.rock_cell):
                    raise ValueError("Cell [" + str(x + width - 1) + ", " + str(y + height - 1) + "] contains rock")
                self.get_area()[self.get_cell_index(x + width - 1, y + height - 1)] = s.get_ship()[s.get_cell_index(width - 1, height - 1)]
                width = width - 1
            height = height - 1


    def remove_ship(self, x: int, y: int):
        """
            Method for removing ship from game area. Method use flood-fill (4-surroundings)

            :param x: x-coordinate of one cell where ship is
            :param y: y-coordinate of one cell where ship is
        """
    
        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate [" + str(x) + ", " + str(y) + "] out of game area")
        if (self.get_area()[self.get_cell_index(x, y)] != user_area.ship_cell):
            raise ValueError("Cell [" + str(x) + ", " + str(y) + "] does not contain")

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


    def generate_ships(self, ship_count: int = 5, max_length: int = 5, tries_to_place: int = 3):
        """
            Method for generating ships – method places 4 random ships into game area

            :param ship_count: Param determine hoe many ships should be generated
            :param max_length: Param set maximun ship cells, defaultly is 5
            :param tries_to_place: Set maximum amount of attemps inserting ship into area

            warnings:: Method can potentionally run for a long time, time can be
                cropped using max_length and tries_to_place params
        """

        if (ship_count <= 0):
            raise ValueError("Method cannot generate " + str(ship_count) + "ships")
        if (max_length <= 0):
            raise ValueError("Ship length must be positive number, not " + str(max_length))
        if (tries_to_place <= 0):
            raise ValueError("Amount of attemps to place ship must be positive, not " + str(tries_to_place))


        while ship_count:
            # generate ship
            s = ship(ship.max_width, ship.max_height)
            cell_counter = max_length
            while cell_counter:
                while True:
                    try:
                        x = randint(0, ship.max_width - 1)
                        y = randint(0, ship.max_height - 1)
                        s.place_ship_cell((x, y))
                        break
                    except ValueError:
                        pass
                cell_counter -= 1
            if (not s.is_ship_continuous()):
                continue
            # place ship into area
            attemp = tries_to_place
            while attemp:
                try:
                    x = randint(0, self.get_x() - s.get_width() - 1)
                    y = randint(0, self.get_y() - s.get_height() - 1)
                    self.place_ship(x, y, s)
                except ValueError:
                    attemp -= 1
            ship_count -= 1
            
 
    def place_unknown_cell(self, x: int, y: int):
        """
            Method for inserting unknown cell (means water) into the game area
            
            :param x: x-part of the coordinate
            :param y: y-part of the coordinate
        """

        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate [" + str(x) + ", " + str(y) + "] out of game area")
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
            raise IndexError("Coordinate [" + str(x) + ", " + str(y) + "] out of game area")
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
            raise IndexError("Coordinate [" + str(x) + ", " + str(y) + "] out of game area")
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
            raise IndexError("Coordinate [" + str(x) + ", " + str(y) + "] out of game area")
        if (self.is_shooted_cell(x, y)):
            raise ValueError("Cell [" + str(x) + ", " + str(y) + "] is already shooted")
        
        if (self.is_cell_ship(x, y)):
            self.get_area()[self.get_cell_index(x, y)] = user_area.shooted_ship_cell
            return True
        else:
            self.get_area()[self.get_cell_index(x, y)] = user_area.shooted_empty_cell
            return False


    def shoot_bomb(self, x: int, y: int) -> bool:
        """
            Method simulating shooting bomb into the player game area
            Method is called when app get "shoot bomb info" from network
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


    def remove_rocks(self):
        """
            Method for removing rocks from user game area 
        """

        for cell in self.get_area():
            if (cell == user_area.rock_cell):
                self.get_area()[self.get_area().index(cell)] = user_area.unknown_cell


    def place_rock_cell(self, x: int, y: int, from_generator: bool = False):
        """
            Method for placing rock cells into game area.

            :param x: x-coordinate of the cell, where rock should be placed
            :param y: y-coordinate of the cell, where rock should be placed
            :param from_generator: param should be True, if method is called from rocks generator method, else should be false.
        """
        if (not from_generator):
            # values from generator is always in game area – no need to check this
            if (not self.is_valid_coordinates(x, y)):
                raise IndexError("Coordinate [" + str(x) + ", " + str(y) + "] out of game area")
        if (self.get_area()[self.get_cell_index(x, y)] != user_area.unknown_cell):
            raise ValueError("Cannot place rock into cell [" + str(x) + ", " + str(y) + "] – cell is not empty")
        
        self.get_area()[self.get_cell_index(x, y)] = user_area.rock_cell


    def generate_rocks(self, amount: int, tries_to_generate: int = maxsize):
        """
            Method for generating random rocks in player game area.
            If there is any rocks before calling this method, they
            will be removed
        
            :param amount: amount of rocks which should be generated
            :param tries_to_generate: amount of attemps for placing one rock cell before cancelling placing

            warnings:: Method can potentionally run for long time due to
                random generated coordintes – you can crop time using tries_to_generate param.
        """
        self.remove_rocks()

        if (amount <= 0):
            raise ValueError("Cannot generate " + str(amount) + "rocks")
        if (amount > self.get_area().count(user_area.unknown_cell)):
            raise ValueError("Cannot generate " + str(amount) + " rocks, game area contains only " + str(self.get_area().count(user_area.unknown_cell)) + " water cells")

        while(amount):
            while True and tries_to_generate:
                try:
                    x = randint(0, self.get_x() - 1)
                    y = randint(0, self.get_y() - 1)
                    self.place_rock_cell(x, y, True)
                    break
                except ValueError:
                    tries_to_generate -= 1
            amount -= 1
