import math
from .vector2d import Vector2d
from .config import RAY_COUNT
from .config import FOV_ANGLE
from .ray import Ray


class FieldOfView():
    def __init__(self, angle: float):
        self.__total_angle_view = FOV_ANGLE
        self.__ang_abs_min = (self.__total_angle_view * -0.5 + math.pi * 2) % (math.pi * 2)
        self.__ang_abs_max = (self.__total_angle_view * 0.5 + math.pi * 2) % (math.pi * 2)
        self.__vector2d_ang_min = Vector2d(1, 0) ** self.__ang_abs_min
        self.__vector2d_ang_max = Vector2d(1, 0) ** self.__ang_abs_max
        self.__vector2d_ang = Vector2d(1, 0)
        ray_count = RAY_COUNT - RAY_COUNT % 2
        ray_angle = FOV_ANGLE / (RAY_COUNT - 1)
        self.__rays = [Ray((c * ray_angle) - (FOV_ANGLE / 2)) for c in range(ray_count)]

        self.rot(angle)

    @property
    def ang(self):
        return self.__vector2d_ang.ang

    @property
    def ang_min(self):
        return self.__vector2d_ang_min.ang

    @property
    def ang_max(self):
        return self.__vector2d_ang_max.ang

    @property
    def rays(self):
        return tuple(self.__rays)

    def rot(self, rad: float):
        self.__vector2d_ang = self.__vector2d_ang ** rad
        self.__vector2d_ang_min = self.__vector2d_ang_min ** rad
        self.__vector2d_ang_max = self.__vector2d_ang_max ** rad
        for ray in self.__rays:
            ray.rot(rad)

    def cast(self, pos: Vector2d):
        pass
