from pyfenstein3d.engine import Decoration
from pyfenstein3d.engine import Wall
from pyfenstein3d.engine import Map2d
from pyfenstein3d.engine import Player

def test_create_with_pattern():
    pattern = "0B010F110A\n3CFF3E  3C"
    map2d = Map2d.create_with_pattern(pattern)
    grid = map2d.grid
    assert isinstance(grid.get_item(0, 0), Wall)
    assert grid.get_item(0, 0).type_id == 11
    assert isinstance(grid.get_item(1, 0), Wall)
    assert grid.get_item(1, 0).type_id == 1
    assert isinstance(grid.get_item(2, 0), Wall)
    assert grid.get_item(2, 0).type_id == 15
    assert isinstance(grid.get_item(3, 0), Wall)
    assert grid.get_item(3, 0).type_id == 17
    assert isinstance(grid.get_item(4, 0), Wall)
    assert grid.get_item(4, 0).type_id == 10

    assert isinstance(grid.get_item(0, 1), Decoration)
    assert grid.get_item(0, 1).type_id == 60
    assert grid.get_item(0, 1).is_solid
    assert isinstance(grid.get_item(1, 1), Player)
    assert isinstance(grid.get_item(2, 1), Decoration)
    assert grid.get_item(2, 1).type_id == 62
    assert not grid.get_item(2, 1).is_solid
    assert grid.get_item(3, 1) is None
    assert isinstance(grid.get_item(4, 1), Decoration)
    assert grid.get_item(4, 1).type_id == 60
    assert grid.get_item(4, 1).is_solid
