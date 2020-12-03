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
    assert map2d.block(0, 0) == item
    assert map2d.block(5, 1) == decoration
    assert map2d.block(10, 15) == decoration_solid
    assert map2d.block(2, 23) == wall
