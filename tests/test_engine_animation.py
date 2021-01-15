from pytest_mock import MockerFixture
from engine import Animation

def test_init(mocker: MockerFixture):
    on_animate = mocker.Mock(return_value=None)
    on_animate_end = mocker.Mock(return_value=None)
    animation = Animation(2, on_animate=on_animate, on_animate_end=on_animate_end)
    assert animation.total_time == 2
    assert animation.time == 0
    assert animation.factor == 0
    assert not animation.is_animating
    animation.start()
    assert animation.total_time == 2
    assert animation.time == 0
    assert animation.factor == 0
    assert animation.is_animating
    animation.update(0.5)
    assert animation.total_time == 2
    assert animation.time == 0.5
    assert animation.factor == 0.25
    assert animation.is_animating
    on_animate.assert_called_with(0.25)
    on_animate_end.assert_not_called()
    animation.update(0.5)
    assert animation.total_time == 2
    assert animation.time == 1
    assert animation.factor == 0.5
    assert animation.is_animating
    on_animate.assert_called_with(0.5)
    on_animate_end.assert_not_called()
    animation.update(1)
    assert animation.total_time == 2
    assert animation.time == 2
    assert animation.factor == 1
    assert not animation.is_animating
    on_animate.assert_called_with(1)
    on_animate_end.assert_called_once()


