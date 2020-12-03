from pyfenstein3d.vector2d import Vector2d
import math


class Item(Vector2d):
    def __init__(self, x: float, y: float, sprite_id: str, is_solid: bool=False):
        super().__init__(x, y)
        self.__sprite_id = sprite_id
        self.__is_solid = is_solid

    @property
    def block_x(self):
        return self.__block_x

    @property
    def block_y(self):
        return self.__block_y

    @property
    def offset_x(self):
        return self.__offset_x

    @property
    def offset_y(self):
        return self.__offset_y

    @property
    def sprite_id(self):
        return self.__sprite_id

    @property
    def is_solid(self):
        return self.__is_solid

    def set_x_y(self, x: float, y: float):
        super().set_x_y(x, y)
        self.__block_x = math.floor(x)
        self.__block_y = math.floor(y)
        self.__offset_x = x % 1
        self.__offset_y = y % 1
    

