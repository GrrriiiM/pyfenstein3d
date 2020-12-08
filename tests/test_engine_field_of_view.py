import math
from pytest_mock import MockerFixture
from pyfenstein3d_engine import FieldOfView

def test_init(mocker: MockerFixture):
    mocker.patch("pyfenstein3d_engine.field_of_view.RAY_COUNT", 4)
    mocker.patch("pyfenstein3d_engine.field_of_view.FOV_ANGLE", math.pi)
    fov = FieldOfView(0)
    assert len(fov.rays) == 4
    assert fov.ang == 0
    assert fov.ang_min == math.pi * 1.5
    assert fov.ang_max == math.pi * 0.5
    fov.rot(math.pi / 2)
    assert fov.ang == math.pi / 2
    assert fov.ang_min == 0
    assert fov.ang_max == math.pi
