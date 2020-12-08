import math
from .vector2d import Vector2d

class Item():
    def __init__(self, vector_x: float, vector_y: float, type_id: int, is_solid: bool=False):
        self._vector2d = Vector2d(vector_x, vector_y)
        self.__type_id = type_id
        self.__is_solid = is_solid
        self._set_x_y(vector_x, vector_y)

    def get_x(self):
        return self._vector2d.x
    x = property(get_x)

    def get_y(self):
        return self._vector2d.y
    y = property(get_y)

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
    def type_id(self):
        return self.__type_id

    @property
    def is_solid(self):
        return self.__is_solid

    def _set_x_y(self, vector_x: float, vector_y: float):
        self._vector2d = Vector2d(vector_x, vector_y)
        self.__block_x = math.floor(vector_x)
        self.__block_y = math.floor(vector_y)
        self.__offset_x = vector_x % 1
        self.__offset_y = vector_y % 1
