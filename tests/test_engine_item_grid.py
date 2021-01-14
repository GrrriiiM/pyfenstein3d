from engine import Decoration
from engine import Wall
from engine import Item
from engine import ItemGrid

def test_init():
    item = Item(0, 0, 10)
    decoration = Decoration(5, 1, 20, False)
    decoration_solid = Decoration(10, 15, 30, True)
    wall = Wall(2, 23, 40)
    grid = ItemGrid([ item, decoration, decoration_solid, wall ])
    assert grid.max_x == 11
    assert grid.max_y == 24
    assert grid.get_block(0, 0) == item
    assert grid.get_block(5, 1) == decoration
    assert grid.get_block(10, 15) == decoration_solid
    assert grid.get_block(2, 23) == wall
