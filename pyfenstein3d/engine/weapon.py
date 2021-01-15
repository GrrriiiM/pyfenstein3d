from .animation import Animation
from .item_grid import ItemGrid

class Weapon():
    def __init__(self, type_id:int, shoot_interval:int):
        self.__type_id = type_id
        self.__shoot_interval = shoot_interval;
        self.__shoot_animation = Animation(self.__shoot_interval)
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

    def update(self, delta_time:float, grid: ItemGrid):
        if self.is_shooting and not self.__shoot_animation.is_animating:
            self.__shoot_animation.start()
            self.__shoot(grid)
        self.__shoot_animation.update(delta_time)

    def __shoot(self, grid: ItemGrid):
        pass

class WeaponPistol(Weapon):
    def __init__(self):
        super().__init__(121, 0.5)
