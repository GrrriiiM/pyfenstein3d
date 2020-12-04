import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'pyfenstein3d')))
from pyfenstein3d.decoration import Decoration
from pyfenstein3d.wall import Wall
from pyfenstein3d.wall import Item
from pyfenstein3d.map2d import Map2d

def test_init():
    item = Item(0, 0, 10)
    decoration = Decoration(5, 1, 20, False)
    decoration_solid = Decoration(10, 15, 30, True)
    wall = Wall(2, 23, 40)
    map2d = Map2d([ item, decoration, decoration_solid, wall ])
    assert map2d.max_x == 11
    assert map2d.max_y == 24
    assert map2d.block(0, 0) == item
    assert map2d.block(5, 1) == decoration
    assert map2d.block(10, 15) == decoration_solid
    assert map2d.block(2, 23) == wall

def test_create_with_pattern():
    pattern = "0B010F110A\n3C  3E  3C"
    map2d = Map2d.create_with_pattern(pattern)
    assert isinstance(map2d.block(0, 0), Wall)
    assert map2d.block(0, 0).type_id == 11
    assert isinstance(map2d.block(1, 0), Wall)
    assert map2d.block(1, 0).type_id == 1
    assert isinstance(map2d.block(2, 0), Wall)
    assert map2d.block(2, 0).type_id == 15
    assert isinstance(map2d.block(3, 0), Wall)
    assert map2d.block(3, 0).type_id == 17
    assert isinstance(map2d.block(4, 0), Wall)
    assert map2d.block(4, 0).type_id == 10

    assert isinstance(map2d.block(0, 1), Decoration)
    assert map2d.block(0, 1).type_id == 60
    assert map2d.block(0, 1).is_solid
    assert map2d.block(1, 1) is None
    assert isinstance(map2d.block(2, 1), Decoration)
    assert map2d.block(2, 1).type_id == 62
    assert not map2d.block(2, 1).is_solid
    assert map2d.block(3, 1) is None
    assert isinstance(map2d.block(4, 1), Decoration)
    assert map2d.block(4, 1).type_id == 60
    assert map2d.block(4, 1).is_solid
    

    
