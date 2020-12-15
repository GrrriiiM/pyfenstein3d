import math
from .vector2d import Vector2d
from abc import abstractmethod
from abc import abstractclassmethod

class Block():
    def __init__(self, vector_x: float, vector_y: float, type_id: int, is_solid: bool=False, is_moveable: bool=False):
        self._vector2d = Vector2d(vector_x, vector_y)
        self.__type_id = type_id
        self._is_solid = is_solid
        self.__is_moveable = is_moveable
        self._set_x_y(vector_x, vector_y)

    @property
    def x(self):
        return self._vector2d.x

    @property
    def y(self):
        return self._vector2d.y

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
        return self._is_solid

    @property
    def is_moveable(self):
        return self.__is_moveable

    def _set_x_y(self, vector_x: float, vector_y: float):
        self._vector2d = Vector2d(vector_x, vector_y)
        self.__block_x = math.floor(vector_x)
        self.__block_y = math.floor(vector_y)
        self.__offset_x = vector_x % 1
        self.__offset_y = vector_y % 1

    @abstractmethod
    def _get_bounds(self, fov_ang: float):
        pass

    def is_in_fov(self, pos: Vector2d, fov_ang: float, fov_delta: float, dist: float):
        bounds = self._get_bounds(fov_ang)
        # fov_ang_min = (fov_ang - (fov_delta * 0.5) + math.pi * 2) % (math.pi * 2)
        # fov_ang_max = (fov_ang + (fov_delta * 0.5) + math.pi * 2) % (math.pi * 2)
        # fov_ang_min, fov_ang_max = (fov_ang_min, fov_ang_max) if fov_ang_min < fov_ang_max else (fov_ang_max, fov_ang_min)
        for bound in bounds:
            bound_pos = (bound - pos) ** -fov_ang
            if dist > bound_pos.mag:
                bound_ang = bound_pos.ang - math.pi * 2 if bound_pos.ang > math.pi else bound_pos.ang
                if fov_delta * -0.5 <= bound_ang <= fov_delta * 0.5:
                    return True
        return False

    
    def interacted(self):
        pass
