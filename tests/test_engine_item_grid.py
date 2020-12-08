from pyfenstein3d_engine import Decoration
from pyfenstein3d_engine import Wall
from pyfenstein3d_engine import Item
from pyfenstein3d_engine import ItemGrid

def test_init():
    item = Item(0, 0, 10)
    decoration = Decoration(5, 1, 20, False)
    decoration_solid = Decoration(10, 15, 30, True)
    wall = Wall(2, 23, 40)
    grid = ItemGrid([ item, decoration, decoration_solid, wall ])
    assert grid.max_x == 11
    assert grid.max_y == 24
    assert grid.get_item(0, 0) == item
    assert grid.get_item(5, 1) == decoration
    assert grid.get_item(10, 15) == decoration_solid
    assert grid.get_item(2, 23) == wall