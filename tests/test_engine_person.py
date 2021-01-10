import math
import pytest
from pytest_mock import MockerFixture
from pyfenstein3d.engine import Person
from pyfenstein3d.engine import FieldOfView

def test_init(mocker: MockerFixture):
    mocker.patch("pyfenstein3d.engine.person.PERSON_MOVEMENT_VELOCITY", 1)
    mocker.patch("pyfenstein3d.engine.person.PERSON_TURN_VELOCITY", math.pi / 2)
    mocker.patch("pyfenstein3d.engine.field_of_view.FOV_ANGLE", math.pi / 2)
    fov = FieldOfView(math.pi)
    person = Person(1, 2, 10, fov)
    assert person.x == 1
    assert person.y == 2
    assert person.fov_ang == math.pi
    person.is_moving_back = True
    person.update(1, None)
    assert person.x == pytest.approx(2)
    assert person.y == pytest.approx(2)
    assert person.fov_ang ==  pytest.approx(math.pi)
    person.is_moving_right = True
    person.update(1, None)
    assert person.x == pytest.approx(2.5)
    assert person.y == pytest.approx(1.5)
    assert person.fov_ang ==  pytest.approx(math.pi)
    person.update(1, None)
    assert person.x == pytest.approx(3)
    assert person.y == pytest.approx(1)
    assert person.fov_ang ==  pytest.approx(math.pi)
    person.is_turning_left = True
    person.update(1, None)
    assert person.x == pytest.approx(2.5)
    assert person.y == pytest.approx(0.5)
    assert person.fov_ang ==  pytest.approx(math.pi/2)
    person.is_moving_front = True
    person.is_moving_right = False
    person.update(1, None)
    assert person.x == pytest.approx(2.5)
    assert person.y == pytest.approx(0.5)
    assert person.fov_ang ==  pytest.approx(0)