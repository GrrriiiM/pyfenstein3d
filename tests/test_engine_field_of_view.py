import math
from pyfenstein3d_engine import FieldOfView

def test_init():
    fov = FieldOfView(0, math.pi)
    assert fov.ang == 0
    assert fov.ang_min == math.pi * 1.5
    assert fov.ang_max == math.pi * 0.5
    fov.rot(math.pi / 2)
    assert fov.ang == math.pi / 2
    assert fov.ang_min == 0
    assert fov.ang_max == math.pi
