from .animation import Animation

class Weapon():
    def __init__(self, type_id:int, shoot_interval:int):
        self.__type_id = type_id
        self.__shoot_interval = shoot_interval;
        self.__shoot_animation = Animation(0.5)
        self.is_shooting = False

    @property
    def type_id(self):
        return self.__type_id

    @property
    def shoot_interval(self):
        return self.__shoot_interval

    @property
    def shoot_animation(self):
        return self.__shoot_animation

    def update(self, delta_time:float, person, grid):
        if self.is_shooting and (not self.__shoot_animation.is_animating or self.__shoot_animation.time > self.__shoot_interval):
            self.__shoot_animation.start()
            person.shoot()
        self.__shoot_animation.update(delta_time)


class WeaponKnife(Weapon):
    def __init__(self):
        super().__init__(120, 0.5)

class WeaponPistol(Weapon):
    def __init__(self):
        super().__init__(121, 0.5)

class WeaponSubmachine(Weapon):
    def __init__(self):
        super().__init__(122, 0.3)

class WeaponMinigun(Weapon):
    def __init__(self):
        super().__init__(123, 0.1)
