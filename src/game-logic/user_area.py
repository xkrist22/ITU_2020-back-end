from ship import ship

class user_area:
    unknown_cell = 0
    ship_cell = 1
    shooted_ship_cell = 2
    shooted_empty_cell = 3


    def __init__(self, width: int, height: int):
        self.__x = width
        self.__y = height
        self.__area = [user_area.unknown_cell] * (width * height)


    def get_area(self) -> list:
        return self.__area


    def is_valid_coordinates(self, x: int, y: int) -> bool:
        if (x > self.get_x() - 1 or y > self.get_y() - 1 or x < 0 or y < 0):
            return False
        else:
            return True
        

    def get_x(self) -> int:
        return self.__x


    def get_y(self) -> int:
        return self.__y


    def get_cell_index(self, x: int, y: int) -> int:
        return (self.get_x() * y) + x


    def place_ship(self, x: int, y: int, s: ship):
        if (not self.is_valid_coordinates(x, y) or not self.is_valid_coordinates(x + s.get_width() - 1, y + s.get_height() - 1)):
            raise IndexError("Coordinate out of game area")
        
        height = s.get_height() 
        while height:
            width = s.get_width()
            while width:
                self.get_area()[self.get_cell_index(x + width - 1, y + height - 1)] = s.get_ship()[s.get_cell_index(width - 1, height - 1)]
                width = width - 1
            height = height - 1

   
    def place_unknown_cell(self, x: int, y: int):
        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of game area")
        self.get_area()[self.get_cell_index(x, y)] = user_area.unknown_cell


    def is_cell_ship(self, x: int, y: int) -> bool:
        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of game area")
        if (self.get_area()[self.get_cell_index(x, y)] == user_area.ship_cell):
            return True
        else:
            return False


    def is_shooted_cell(self, x: int, y: int) -> bool:
        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of game area")
        if (self.get_area()[self.get_cell_index(x, y)] == user_area.shooted_empty_cell or self.get_area()[self.get_cell_index(x, y)] == user_area.shooted_ship_cell):
            return True
        else:
            return False


    def shoot(self, x: int, y: int) -> bool:
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
        if user_area.ship_cell in self.get_area():
            return False
        else:
            return True
