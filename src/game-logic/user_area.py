class user_area:
    unknown_cell = 0
    ship_cell = 1
    shooted_ship_cell = 2
    shooted_empty_cell = 3


    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__area = [user_area.unknown_cell] * (x*y)


    def get_area(self):
        return self.__area


    def is_valid_coordinates(self, x, y):
        if (x > self.get_x() - 1 or y > self.get_y() - 1 or x < 0 or y < 0):
            return False
        else:
            return True
        

    def get_x(self):
        return self.__x


    def get_y(self):
        return self.__y


    def get_cell_index(self, x, y):
        return (self.get_x() * y) + x


    def place_ship_cell(self, x, y):
        if (not self.is_valid_coordinates(x, y)):
            raise ValueError
        self.get_area()[self.get_cell_index(x, y)] = user_area.ship_cell
        return True

    
    def place_unknown_cell(self, x, y):
        if (not self.is_valid_coordinates(x, y)):
            raise ValueError
        self.get_area()[self.get_cell_index(x, y)] = user_area.unknown_cell
        return True


    def is_cell_ship(self, x, y):
        if (not self.is_valid_coordinates(x, y)):
            raise ValueError
        if (self.get_area()[self.get_cell_index(x, y)] == user_area.ship_cell):
            return True
        else:
            return False

    def is_shooted_cell(self, x, y):
        if (not self.is_valid_coordinates(x, y)):
            raise ValueError
        if (self.get_area()[self.get_cell_index(x, y)] == user_area.shooted_empty_cell or self.get_area()[self.get_cell_index(x, y)] == user_area.shooted_ship_cell):
            return True
        else:
            return False



    def shoot(self, x, y):
        if (not self.is_valid_coordinates(x, y)):
            raise ValueError
        if (self.is_shooted_cell(x, y)):
            raise ValueError
        
        if (self.is_cell_ship(x, y)):
            self.get_area()[self.get_cell_index(x, y)] = user_area.shooted_ship_cell
            return True
        else:
            self.get_area()[self.get_cell_index(x, y)] = user_area.shooted_empty_cell
            return False


    def all_ships_shooted(self):
        if user_area.ship_cell in self.get_area():
            return False
        else:
            return True

