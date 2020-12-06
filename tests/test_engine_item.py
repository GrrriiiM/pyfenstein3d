from pyfenstein3d_engine import Item


def test_init():
    item = Item(1.5, 3.7, 20, is_solid=True)
    assert item.x == 1.5
    assert item.y == 3.7
    assert item.block_x == 1
    assert item.block_y == 3
    assert round(item.offset_x, 1) == 0.5
    assert round(item.offset_y, 1) == 0.7
    assert item.is_solid
