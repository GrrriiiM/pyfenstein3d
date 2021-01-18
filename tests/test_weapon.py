from engine import Weapon
from engine import Player

def test_shoot():
    weapon = Weapon(10, 0.5)
    grid = None
    person = Player(0, 0, 0, None, "")
    assert weapon.shoot_interval == 0.5;
    assert weapon.is_shooting == False
    assert weapon.shoot_animation.is_animating == False
    assert weapon.shoot_animation.factor == 0
    weapon.update(0.1, person, grid)
    assert weapon.is_shooting == False
    assert weapon.shoot_animation.is_animating == False
    assert weapon.shoot_animation.factor == 0
    weapon.is_shooting = True
    assert weapon.is_shooting == True
    assert weapon.shoot_animation.is_animating == False
    assert weapon.shoot_animation.factor == 0
    weapon.update(0.1, person, grid)
    assert weapon.is_shooting == True
    assert weapon.shoot_animation.is_animating == True
    assert weapon.shoot_animation.factor == 0.2
    weapon.update(0.1, person, grid)
    assert weapon.is_shooting == True
    assert weapon.shoot_animation.is_animating == True
    assert weapon.shoot_animation.factor == 0.4
    weapon.update(0.3, person, grid)
    assert weapon.is_shooting == True
    assert weapon.shoot_animation.is_animating == False
    assert weapon.shoot_animation.factor == 1
    weapon.update(0.3, person, grid)
    assert weapon.is_shooting == True
    assert weapon.shoot_animation.is_animating == True
    assert weapon.shoot_animation.factor == 0.6
    weapon.is_shooting = False
    weapon.update(0.3, person, grid)
    assert weapon.is_shooting == False
    assert weapon.shoot_animation.is_animating == False
    assert weapon.shoot_animation.factor == 1
    weapon.update(0.3, person, grid)
    assert weapon.is_shooting == False
    assert weapon.shoot_animation.is_animating == False
    assert weapon.shoot_animation.factor == 0