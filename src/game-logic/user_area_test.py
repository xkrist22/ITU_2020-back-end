import user_area as ua
import pytest

@pytest.fixture
def area():
    return ua.user_area(10, 10)


@pytest.fixture
def area_with_boat():
    area = ua.user_area(10, 10)
    area.place_ship_cell(0, 0)
    area.place_ship_cell(1, 0)
    area.place_ship_cell(2, 0)
    area.place_ship_cell(1, 1)
    return area


def test_user_area_creating(area):
    assert(isinstance(area.get_area(), list))


def test_user_area_length(area):
    assert(len(area.get_area()) == 100)


def test_user_area_values(area):
    assert (all(item == ua.user_area.unknown_cell for item in area.get_area()))


def test_user_area_contain_boat(area):
    area.place_ship_cell(0, 0)
    assert (ua.user_area.ship_cell in area.get_area())
    assert(area.get_area()[0] == ua.user_area.ship_cell)


def test_user_remove_boat(area_with_boat):
    area_with_boat.place_unknown_cell(0, 0)
    area_with_boat.place_unknown_cell(1, 0)
    area_with_boat.place_unknown_cell(2, 0)
    area_with_boat.place_unknown_cell(1, 1)
    assert (all(item == ua.user_area.unknown_cell for item in area_with_boat.get_area()))


def test_shoot_at_ship(area_with_boat):
    area_with_boat.shoot(1,0)
    assert(ua.user_area.shooted_ship_cell in area_with_boat.get_area())


def test_shoot_into_water(area_with_boat):
    area_with_boat.shoot(5, 5)
    assert(ua.user_area.shooted_empty_cell in area_with_boat.get_area())


def test_shooting_again_into_ship(area_with_boat):
    area_with_boat.shoot(1,0)
    with pytest.raises(ValueError):
        area_with_boat.shoot(1,0)

    area_with_boat.shoot(5,5)
    with pytest.raises(ValueError):
        area_with_boat.shoot(5,5)
        

def test_error_values(area_with_boat):
    with pytest.raises(ValueError):
        area_with_boat.place_ship_cell(42, 42)
        area_with_boat.place_ship_cell(10, 10)
        area_with_boat.place_unknown_cell(42, 42)
        area_with_boat.place_unknown_cell(10, 10)
        area_with_boat.shoot(42, 42)
        area_with_boat.shoot(10, 10)
