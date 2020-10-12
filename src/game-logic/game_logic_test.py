from user_area import user_area
from ship import ship
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


def test_user_area_creating(area):
    assert(isinstance(area.get_area(), list))


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
    with pytest.raises(IndexError):
        area_with_boat.shoot(1,0)

    area_with_boat.shoot(5,5)
    with pytest.raises(IndexError):
        area_with_boat.shoot(5,5)
        

def test_error_values(area_with_boat):
    with pytest.raises(IndexError):
        area_with_boat.place_unknown_cell(42, 42)
        area_with_boat.place_unknown_cell(10, 10)
        area_with_boat.shoot(42, 42)
        area_with_boat.shoot(10, 10)
    s = ship(1, 1)
    s.place_ship_cell((0, 0))
    with pytest.raises(IndexError):
        area_with_boat.place_ship(42, 42, s)


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


def test_print_ship(area_with_boat):
    print(area_with_boat.get_area())


def test_removing_ship(area_with_boat):
    area_with_boat.remove_ship(0, 0)
    assert(not user_area.ship_cell in area_with_boat.get_area())

def test_continuousity_ship(continuous_ship, uncontinuous_ship):
    assert(continuous_ship.is_ship_continuous())
    assert(not uncontinuous_ship.is_ship_continuous())