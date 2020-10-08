import random


class enemy_area:
    unknown_cell = 0
    shooted_ship_cell = 2
    shooted_empty_cell = 3


    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__area = [enemy_area.unknown_cell] * (x*y)


    def get_area(self):
        return self.__area


    def is_valid_coordinates(self, x, y):
        if (x > self.get_x() - 1 or y > self.get_y() - 1 or x < 0 or y < 0):
            return False
        else:
            return True


    def is_shooted_cell(self, x, y):
        if (not self.is_valid_coordinates(x, y)):
            raise ValueError
        if (self.get_area()[self.get_cell_index(x, y)] == enemy_area.shooted_empty_cell or self.get_area()[self.get_cell_index(x, y)] == enemy_area.shooted_ship_cell):
            return True
        else:
            return False


    def get_x(self):
        return self.__x


    def get_y(self):
        return self.__y


    def get_cell_index(self, x, y):
        return (self.get_x() * y) + x


    # method for simulated shooting
    # should be replaced by network communication
    def shooting_stub(self):
        if (random.randint(0, 100) % 2 == 0):
            return True
        else:
            return False 


    def shoot(self, x, y):
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
