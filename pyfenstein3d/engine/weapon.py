from .animation import Animation
from .item_grid import ItemGrid

class Weapon():
    def __init__(self, type_id:int, shoot_interval:int):
        self.__type_id = type_id
        self.__shoot_interval = shoot_interval;
        self.__shoot_animation = Animation(self.__shoot_interval)
        self.__is_shooting = False

    @property
    def shoot_interval(self):
        return self.__shoot_interval

    @property
    def is_shooting(self):
        return self.__is_shooting

    @property
    def shoot_animation(self):
        return self.__shoot_animation

    def start_shooting(self):
        self.__is_shooting = True

    def stop_shooting(self):
        self.__is_shooting = False

    def update(self, delta_time:float, grid: ItemGrid):
        if self.__is_shooting and not self.__shoot_animation.is_animating:
            self.__shoot_animation.start()
            self.__shoot(grid)
        self.__shoot_animation.update(delta_time)

    def __shoot(self, grid: ItemGrid):
        pass

class WeaponPistol(Weapon):
    def __init__(self):
        super().__init__(251, 1)
