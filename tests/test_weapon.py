from engine import Weapon

def test_shoot():
    weapon = Weapon(10, 0.5)
    grid = None
    assert weapon.shoot_interval == 0.5;
    assert weapon.is_shooting == False
    assert weapon.shoot_animation.is_animating == False
    assert weapon.shoot_animation.factor == 0
    weapon.update(0.1, grid)
    assert weapon.is_shooting == False
    assert weapon.shoot_animation.is_animating == False
    assert weapon.shoot_animation.factor == 0
    weapon.start_shooting()
    assert weapon.is_shooting == True
    assert weapon.shoot_animation.is_animating == False
    assert weapon.shoot_animation.factor == 0
    weapon.update(0.1, grid)
    assert weapon.is_shooting == True
    assert weapon.shoot_animation.is_animating == True
    assert weapon.shoot_animation.factor == 0.2
    weapon.update(0.1, grid)
    assert weapon.is_shooting == True
    assert weapon.shoot_animation.is_animating == True
    assert weapon.shoot_animation.factor == 0.4
    weapon.update(0.3, grid)
    assert weapon.is_shooting == True
    assert weapon.shoot_animation.is_animating == False
    assert weapon.shoot_animation.factor == 1
    weapon.update(0.3, grid)
    assert weapon.is_shooting == True
    assert weapon.shoot_animation.is_animating == True
    assert weapon.shoot_animation.factor == 0.6
    weapon.stop_shooting()
    weapon.update(0.3, grid)
    assert weapon.is_shooting == False
    assert weapon.shoot_animation.is_animating == False
    assert weapon.shoot_animation.factor == 1
    weapon.update(0.3, grid)
    assert weapon.is_shooting == False
    assert weapon.shoot_animation.is_animating == False
    assert weapon.shoot_animation.factor == 0