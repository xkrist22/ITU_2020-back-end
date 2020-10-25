from user_area import user_area
from ship import ship
from enemy_area import enemy_area
import pytest

@pytest.fixture
def area():
    return user_area(10, 10)


@pytest.fixture
def area_with_boat():
    area = user_area(10, 10)
    s = ship(3, 2)
    s.place_ship_cell((0, 0), (1, 0), (2, 0), (1, 1))
    area.place_ship(0, 0, s)
    return area


@pytest.fixture
def continuous_ship():
    s = ship(3, 2)
    s.place_ship_cell((0, 0), (1, 0), (2, 0), (1, 1))
    return s


@pytest.fixture
def uncontinuous_ship():
    s = ship(3, 3)
    s.place_ship_cell((0, 0), (2, 2))
    return s


@pytest.fixture
def enemy():
    return enemy_area(10, 10)


@pytest.fixture
def area_with_rocks():
    a = user_area(6, 6)
    a.place_rock_cell(0, 0)
    return a


@pytest.fixture
def huge_area():
    return user_area(10000, 10000)


def test_user_area_creating(area):
    assert(isinstance(area.get_area(), list))
    with pytest.raises(ValueError):
        user_area(0, 0)
        user_area(10, 5)
        user_area(-3, 10)


def test_user_area_length(area):
    assert(len(area.get_area()) == 100)


def test_user_area_values(area):
    assert (all(item == user_area.unknown_cell for item in area.get_area()))


def test_user_area_contain_boat(area_with_boat):
    assert (user_area.ship_cell in area_with_boat.get_area())
    assert(area_with_boat.get_area()[0] == user_area.ship_cell)
    assert(area_with_boat.get_area()[1] == user_area.ship_cell)
    assert(area_with_boat.get_area()[2] == user_area.ship_cell)
    assert(area_with_boat.get_area()[11] == user_area.ship_cell)


def test_user_remove_boat(area_with_boat):
    area_with_boat.place_unknown_cell(0, 0)
    area_with_boat.place_unknown_cell(1, 0)
    area_with_boat.place_unknown_cell(2, 0)
    area_with_boat.place_unknown_cell(1, 1)
    assert (all(item == user_area.unknown_cell for item in area_with_boat.get_area()))


def test_shoot_at_ship(area_with_boat):
    area_with_boat.shoot(1,0)
    assert(user_area.shooted_ship_cell in area_with_boat.get_area())


def test_shoot_into_water(area_with_boat):
    area_with_boat.shoot(5, 5)
    assert(user_area.shooted_empty_cell in area_with_boat.get_area())


def test_shooting_again_into_ship(area_with_boat):
    area_with_boat.shoot(1,0)
    with pytest.raises(ValueError):
        area_with_boat.shoot(1,0)

    area_with_boat.shoot(5,5)
    with pytest.raises(ValueError):
        area_with_boat.shoot(5,5)
        

def test_error_values(area_with_boat):
    with pytest.raises(IndexError):
        # test non existing coordinates
        area_with_boat.place_unknown_cell(42, 42)
        area_with_boat.place_unknown_cell(10, 10)
        area_with_boat.shoot(42, 42)
        area_with_boat.shoot(10, 10)
    s = ship(1, 1)
    s.place_ship_cell((0, 0))
    # place new ship into non existing coordinates
    with pytest.raises(IndexError):
        area_with_boat.place_ship(42, 42, s)
    # place new ship onto existing ship
    with pytest.raises(ValueError):
        area_with_boat.place_ship(0, 0, s)


def test_ship_creating():
    s = ship(3, 2)
    assert(len(s) == 6)
    s.place_ship_cell((0, 0), (1, 0), (2, 0), (1, 1))
    assert(s.get_ship()[0] == ship.ship_cell)
    assert(s.get_ship()[1] == ship.ship_cell)
    assert(s.get_ship()[2] == ship.ship_cell)
    assert(s.get_ship()[4] == ship.ship_cell)
    assert(s.get_ship()[3] == ship.unknown_cell)
    assert(s.get_ship()[5] == ship.unknown_cell)

    with pytest.raises(ValueError):
        ship(42, 1)
        ship(1, 42)
    with pytest.raises(IndexError):
        ship(-2, 1)
        ship(1, -2)
        ship(0, 1)
        ship(1, 0)
        ship(0, 0)


def test_print_ship(area_with_boat):
    print(area_with_boat.get_area())


def test_removing_ship(area_with_boat):
    area_with_boat.remove_ship(0, 0)
    assert(not user_area.ship_cell in area_with_boat.get_area())

def test_continuousity_ship(continuous_ship, uncontinuous_ship):
    assert(continuous_ship.is_ship_continuous())
    assert(not uncontinuous_ship.is_ship_continuous())


def test_shooting_bomb(area_with_boat):
    area_with_boat.shoot_bomb(1, 1)
    assert(not user_area.ship_cell in area_with_boat.get_area())
    assert(user_area.shooted_ship_cell in area_with_boat.get_area())
    assert(user_area.shooted_empty_cell in area_with_boat.get_area())


def test_shoot_bomb_into_enemy_area(enemy):
    with pytest.raises(IndexError):
        enemy.shoot_bomb(0, 0)
        enemy.shoot_bomb(0, 1)
        enemy.shoot_bomb(1, 0)
        enemy.shoot_bomb(10, 10)
        enemy.shoot_bomb(10, 0)
        enemy.shoot_bomb(0, 10)
        enemy.shoot_bomb(-5, 0)
        enemy.shoot_bomb(-5, -42)
    
    # cannot determine return value due to using shooting_stub
    # i am trying if method does not raise unexpected error
    enemy.shoot_bomb(5, 5)
    enemy.shoot_bomb(1, 1)
    

def test_generating_rocks(area):
    area.generate_rocks(10)
    assert(user_area.rock_cell in area.get_area())
    assert(area.get_area().count(user_area.rock_cell) == 10)
    area.remove_rocks()
    assert(not user_area.rock_cell in area.get_area())
    # try to generate map containing only rocks
    area.generate_rocks(100)

    with pytest.raises(ValueError):
        area.generate_rocks(101)
        area.generate_rocks(-5)
        area.generate_rocks(0)


def test_rocks(area_with_rocks):
    s = ship(1, 1)
    s.place_ship_cell((0, 0))
    with pytest.raises(ValueError):
        area_with_rocks.place_ship(0, 0, s)
    with pytest.raises(IndexError):
        area_with_rocks.place_ship(-1, 0, s)
        area_with_rocks.place_ship(0, -42, s)
        area_with_rocks.place_ship(42, 42, s)


def test_generating_ships(area):
    area.generate_ships()
    assert(user_area.ship_cell in area.get_area())

