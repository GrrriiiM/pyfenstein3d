import math
from .vector2d import Vector2d

class FieldOfView(Vector2d):
    def __init__(self, angle_direction: float, total_angle_view: float):
        self.__total_angle_view = total_angle_view
        self.__ang_abs_min = total_angle_view / -2
        self.__ang_abs_max = total_angle_view / 2
        self.__min = Vector2d(1, 0)
        self.__min.rot(self.__ang_abs_min)
        self.__max = Vector2d(1, 0)
        self.__max.rot(self.__ang_abs_max)
        super().__init__(1, 0)
        self.rot(angle_direction)

    @property
    def ang_min(self):
        return self.__min.ang

    @property
    def ang_max(self):
        return self.__max.ang

    def set_x_y(self, vector_x: float, vector_y: float):
        mag = math.sqrt(math.pow(vector_x, 2) + math.pow(vector_y, 2))
        if mag == 0:
            super().set_x_y(1, 0)
        else:
            super().set_x_y(vector_x / mag, vector_y / mag)
        self.__min.rot(self.ang)
        self.__max.rot(self.ang)
