class ship:
    unknown_cell = 0
    ship_cell = 1
    max_width = 5
    max_height = 3


    def __init__(self, width: int, height: int):
        if (width > ship.max_width):
            raise ValueError("Max width of the ship is 5")
        if (height > ship.max_height):
            raise ValueError("Max height of the ship is 3")
        self.__width = width
        self.__height = height
        self.__ship_array = [ship.unknown_cell] * (width * height)


    def __len__(self) -> int:
        return len(self.get_ship())


    def get_ship(self) -> list:
        return self.__ship_array


    def is_valid_coordinates(self, x: int, y: int) -> bool:
        if (x > self.get_width() - 1 or y > self.get_height() - 1 or x < 0 or y < 0):
            return False
        else:
            return True
        

    def get_width(self) -> int:
        return self.__width


    def get_height(self) -> int:
        return self.__height


    def get_cell_index(self, x: int, y: int) -> int:
        return (self.get_width() * y) + x


    def place_ship_cell(self, *coordinates: tuple):
        for x, y in coordinates:
            if (not self.is_valid_coordinates(x, y)):
                raise IndexError("Coordinate out of ship area")
            self.get_ship()[self.get_cell_index(x, y)] = ship.ship_cell


    def place_unknown_cell(self, x: int, y: int):
        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of ship area")
        self.get_ship()[self.get_cell_index(x, y)] = ship.unknown_cell


    def is_cell_ship(self, x: int, y: int) -> bool:
        if (not self.is_valid_coordinates(x, y)):
            raise IndexError("Coordinate out of ship area")
        if (self.get_ship()[self.get_cell_index(x, y)] == ship.ship_cell):
            return True
        else:
            return False
