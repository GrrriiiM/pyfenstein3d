import math
import pytest
from pytest_mock import MockerFixture
from pyfenstein3d_engine import Person
from pyfenstein3d_engine import FieldOfView

def test_init(mocker: MockerFixture):
    mocker.patch("pyfenstein3d_engine.person.PERSON_MOVEMENT_VELOCITY", 1)
    mocker.patch("pyfenstein3d_engine.person.PERSON_TURN_VELOCITY", math.pi / 2)
    fov = FieldOfView(math.pi, math.pi / 2)
    person = Person(1, 2, 10, fov)
    assert person.x == 1
    assert person.y == 2
    assert person.fov_ang == math.pi
    person.is_moving_back = True
    person.update()
    assert person.x == pytest.approx(2)
    assert person.y == pytest.approx(2)
    assert person.fov_ang ==  pytest.approx(math.pi)
    person.is_moving_right = True
    person.update()
    assert person.x == pytest.approx(2.5)
    assert person.y == pytest.approx(1.5)
    assert person.fov_ang ==  pytest.approx(math.pi)
    person.update()
    assert person.x == pytest.approx(3)
    assert person.y == pytest.approx(1)
    assert person.fov_ang ==  pytest.approx(math.pi)
    person.is_turning_left = True
    person.update()
    assert person.x == pytest.approx(2.5)
    assert person.y == pytest.approx(0.5)
    assert person.fov_ang ==  pytest.approx(math.pi/2)
    person.is_moving_front = True
    person.is_moving_right = False
    person.update()
    assert person.x == pytest.approx(2.5)
    assert person.y == pytest.approx(0.5)
    assert person.fov_ang ==  pytest.approx(0)