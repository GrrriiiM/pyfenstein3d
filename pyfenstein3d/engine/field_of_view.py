import math
from .vector2d import Vector2d
from .config import RAY_COUNT
from .config import FOV_ANGLE
from .ray import Ray


class FieldOfView():
    def __init__(self, angle: float):
        self.__ang_abs_min = (FOV_ANGLE * -0.5 + math.pi * 2) % (math.pi * 2)
        self.__ang_abs_max = (FOV_ANGLE * 0.5 + math.pi * 2) % (math.pi * 2)
        self.__vector2d_ang_min = Vector2d(1, 0) ** self.__ang_abs_min
        self.__vector2d_ang_max = Vector2d(1, 0) ** self.__ang_abs_max
        self.__vector2d_ang = Vector2d(1, 0)
        self.__dist = 0
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

    def cast(self, player, grid):
        pos = Vector2d(player.x, player.y)
        for ray in self.__rays:
            ray.cast_wall(pos, grid)
            if ray.dist > self.__dist:
                self.__dist = ray.dist

        dist = max([ray.dist for ray in self.__rays])
        doors = grid.get_doors_by_fov(pos, self.ang, FOV_ANGLE, dist)
        for ray in self.__rays:
            ray.cast_doors(pos, doors)
            if ray.dist > self.__dist:
                self.__dist = ray.dist

        dist = max([ray.dist for ray in self.__rays])
        items = grid.get_items_by_fov(pos, self.ang, FOV_ANGLE, dist)
        for ray in self.__rays:
            ray.cast_items(player, items)
