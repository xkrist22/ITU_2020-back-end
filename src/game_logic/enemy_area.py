import random


class enemy_area:
    unknown_cell = 0
    shooted_ship_cell = 2
    shooted_empty_cell = 3


    def __init__(self, width: int, height: int):
        self.__x = width
        self.__y = height
        self.__area = [enemy_area.unknown_cell] * (width * height)


    def get_area(self) -> list:
        return self.__area


    def is_valid_coordinates(self, x: int, y: int) -> bool:
        if (x > self.get_x() - 1 or y > self.get_y() - 1 or x < 0 or y < 0):
            return False
        else:
            return True


    def is_shooted_cell(self, x: int, y: int) -> bool:
        if (not self.is_valid_coordinates(x, y)):
            raise ValueError
        if (self.get_area()[self.get_cell_index(x, y)] == enemy_area.shooted_empty_cell or self.get_area()[self.get_cell_index(x, y)] == enemy_area.shooted_ship_cell):
            return True
        else:
            return False


    def get_x(self) -> int:
        return self.__x


    def get_y(self) -> int:
        return self.__y


    def get_cell_index(self, x: int, y: int) -> int:
        return (self.get_x() * y) + x


    # method for simulated shooting
    # should be replaced by network communication
    def shooting_stub(self) -> int:
        if (random.randint(0, 100) % 2 == 0):
            return True
        else:
            return False 


    def can_shoot(self, x: int, y: int) -> bool:
        if (not self.is_valid_coordinates(x, y)):
            return False
        if (self.is_shooted_cell(x, y)):
            return False
        return True
    
    def shoot(self, x: int, y: int):
        if (not self.is_valid_coordinates(x, y)):
            raise ValueError
        if (self.is_shooted_cell(x, y)):
            raise ValueError
        
        #TODO network communication – is selected cell ship, or water
        is_ship = self.shooting_stub() # this info should be extracted from network communication

        if (is_ship):
            self.get_area()[self.get_cell_index(x, y)] = enemy_area.shooted_ship_cell
        else:
            self.get_area()[self.get_cell_index(x, y)] = enemy_area.shooted_empty_cell
