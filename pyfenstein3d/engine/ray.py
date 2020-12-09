import math
from .vector2d import Vector2d
from .wall import Wall
from .item_grid import ItemGrid


class Ray():
    def __init__(self, angle: float):
        self.__dist_adjusted = 0
        self.__wall_collided: Wall = None
        self.__wall_collided_offset: 0
        self.__wall_collided_is_vertical: False
        self.__wall_collided_is_inverted: False
        self.__rel_ang = angle
        self.__vector2d_ang = Vector2d(1, 0)
        self.__vector2d = Vector2d(0, 0)
        self.rot(angle)

    @property
    def ang(self):
        return self.__vector2d_ang.ang

    @property
    def dir_x(self):
        return self.__dir_x

    @property
    def dir_y(self):
        return self.__dir_y

    @property
    def delta_dist_x(self):
        return self.__delta_dist_x

    @property
    def delta_dist_y(self):
        return self.__delta_dist_y

    @property
    def wall(self):
        return self.__wall_collided

    @property
    def offset(self):
        return self.__wall_collided_offset

    @property
    def is_vertical(self):
        return self.__wall_collided_is_vertical

    @property
    def is_inverted(self):
        return self.__wall_collided_is_inverted

    @property
    def dist(self):
        return self.__dist_adjusted

    @property
    def collided_vector2d(self) -> Vector2d:
        return self.__vector2d

    def cast_wall(self, pos: Vector2d, grid: ItemGrid):
        dist_x = self.get_dist_x(pos)
        dist_y = self.get_dist_y(pos)
        block_x = math.floor(pos.x)
        block_y = math.floor(pos.y)
        while 0 <= block_x < grid.max_x or 0 <= block_y < grid.max_y:
            if dist_y < dist_x:
                block_y += self.dir_y
                item = grid.get_item(block_x, block_y)
                if isinstance(item, Wall):
                    self.__vector2d = Vector2d(
                        math.cos(self.ang) * dist_y,
                        math.sin(self.ang) * dist_y
                    ) + pos
                    self.__dist_adjusted = abs(math.cos(self.__rel_ang) * dist_y)
                    self.__wall_collided = item
                    self.__wall_collided_is_inverted = pos.y > item.y
                    self.__wall_collided_offset = self.__vector2d.x % 1
                    self.__wall_collided_is_vertical = False
                    return
                dist_y += self.delta_dist_y
            else:
                block_x += self.dir_x
                item = grid.get_item(block_x, block_y)
                if isinstance(item, Wall):
                    self.__vector2d = Vector2d(
                        math.cos(self.ang) * dist_x,
                        math.sin(self.ang) * dist_x
                    ) + pos
                    self.__dist_adjusted = abs(math.cos(self.__rel_ang) * dist_x)
                    self.__wall_collided = item
                    self.__wall_collided_is_inverted = pos.x > item.x
                    self.__wall_collided_offset = self.__vector2d.y % 1
                    self.__wall_collided_is_vertical = True
                    return
                dist_x += self.delta_dist_x

    def rot(self, rad):
        self.__vector2d_ang = self.__vector2d_ang ** rad

        if self.ang > math.pi * 1.5 or self.ang < math.pi * 0.5:
            self.__dir_x = 1
        elif self.ang > math.pi * 0.5 and self.ang < math.pi * 1.5:
            self.__dir_x = -1
        else:
            self.__dir_x = 0

        if self.ang > 0 and self.ang < math.pi:
            self.__dir_y = 1
        elif self.ang > math.pi and self.ang < math.pi * 2:
            self.__dir_y = -1
        else:
            self.__dir_y = 0

        self.__delta_dist_x = abs(1 / math.cos(self.ang)) if math.cos(self.ang) != 0 else math.inf
        self.__delta_dist_y = abs(1 / math.sin(self.ang)) if math.sin(self.ang) != 0 else math.inf

    def get_dist_x(self, pos: Vector2d):
        if self.dir_x == 1:
            return abs((1 - pos.x % 1) / math.cos(self.ang))
        if self.dir_x == -1:
            return abs((pos.x % 1) / math.cos(self.ang))
        return math.inf

    def get_dist_y(self, pos: Vector2d):
        if self.dir_y == 1:
            return abs((1 - pos.y % 1) / math.sin(self.ang))
        if self.dir_y == -1:
            return abs((pos.y % 1) / math.sin(self.ang))
        return math.inf
