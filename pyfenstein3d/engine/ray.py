import math
from .vector2d import Vector2d
from .wall import Wall
from .item import Item
from .door import Door


class Ray():
    def __init__(self, angle: float):
        self.__dist_adjusted = 0
        self.__dist = 0
        self.__offset: 0
        self.__is_vertical: False
        self.__is_inverted: False
        self.__type_id: int = None
        self.__rel_ang = angle
        self.__vector2d_ang = Vector2d(1, 0)
        self.__vector2d = Vector2d(0, 0)
        self.__items = []
        self.__doors = []
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
    def type_id(self):
        return self.__type_id

    @property
    def offset(self):
        return self.__offset

    @property
    def is_vertical(self):
        return self.__is_vertical

    @property
    def is_inverted(self):
        return self.__is_inverted

    @property
    def dist_adjusted(self):
        return self.__dist_adjusted

    @property
    def dist(self):
        return self.__dist

    @property
    def collided_vector2d(self) -> Vector2d:
        return self.__vector2d

    @property
    def items(self):
        return tuple(self.__items)

    @property
    def doors(self):
        return tuple(self.__doors)

    def cast_wall(self, pos: Vector2d, grid):
        dist_x = self.get_dist_x(pos)
        dist_y = self.get_dist_y(pos)
        block_x = math.floor(pos.x)
        block_y = math.floor(pos.y)
        while 0 <= block_x < grid.max_x or 0 <= block_y < grid.max_y:
            if dist_y < dist_x:
                block_y += self.dir_y
                item = grid.get_block(block_x, block_y)
                if isinstance(item, Wall):
                    self.__vector2d = Vector2d(
                        math.cos(self.ang) * dist_y,
                        math.sin(self.ang) * dist_y
                    ) + pos
                    self.__dist_adjusted = abs(
                        math.cos(self.__rel_ang) * dist_y)
                    self.__dist = abs(dist_y)
                    self.__is_inverted = pos.y > item.y
                    self.__offset = self.__vector2d.x % 1
                    self.__is_vertical = False
                    if self.__is_inverted and isinstance(grid.get_block(block_x, block_y + 1), Door):
                        self.__type_id = 50
                    elif not self.__is_inverted and isinstance(grid.get_block(block_x, block_y - 1), Door):
                        self.__type_id = 50
                    else:
                        self.__type_id = item.type_id

                    return
                dist_y += self.delta_dist_y
            else:
                block_x += self.dir_x
                item = grid.get_block(block_x, block_y)
                if isinstance(item, Wall):
                    self.__vector2d = Vector2d(
                        math.cos(self.ang) * dist_x,
                        math.sin(self.ang) * dist_x
                    ) + pos
                    self.__dist_adjusted = abs(
                        math.cos(self.__rel_ang) * dist_x)
                    self.__dist = abs(dist_x)
                    self.__is_inverted = pos.x > item.x
                    self.__offset = self.__vector2d.y % 1
                    self.__is_vertical = True
                    if self.__is_inverted and isinstance(grid.get_block(block_x + 1, block_y), Door):
                        self.__type_id = 50
                    elif not self.__is_inverted and isinstance(grid.get_block(block_x - 1, block_y), Door):
                        self.__type_id = 50
                    else:
                        self.__type_id = item.type_id
                    return
                dist_x += self.delta_dist_x

    def cast_doors(self, pos: Vector2d, doors: []):
        self.__doors = []
        for door in doors:
            if door.is_vertical:
                is_inverted = math.pi * 0.5 <= self.ang <= math.pi * 1.5
                if not is_inverted and  door.x > self.__vector2d.x:
                    continue
                if is_inverted and door.x < self.__vector2d.x:
                    continue
                x = door.x - pos.x;
                y = math.tan(self.ang) * x;
                v = Vector2d(x, y);
                pos_y = pos.y + y;
                if pos_y < door.y or pos_y > door.y + 1:
                    continue
                dist_adjusted = math.sin(math.pi / 2 - self.__rel_ang) * v.mag;
                offset = (door.y - pos_y) % 1 #- Math.floor(door.y - pos_y);
                self.__doors.append(RayDoor(dist_adjusted, offset, door.is_vertical))
                if v.mag < self.__dist:
                    self.__dist = v.mag
                    self.__vector2d = v + pos
                    self.__dist_adjusted = dist_adjusted
            else:
                is_inverted = math.pi <= self.ang <= math.pi * 2
                if not is_inverted and door.y > self.__vector2d.y:
                    continue
                if is_inverted and door.y < self.__vector2d.y:
                    continue
                y = door.y - pos.y
                x = y / math.tan(self.ang)
                v = Vector2d(x, y)
                pos_x = pos.x + x
                if pos_x < door.x or pos_x > door.x + 1:
                    continue
                dist_adjusted = math.sin(math.pi / 2 - self.__rel_ang) * v.mag
                offset = (door.x - pos_x) % 1
                self.__doors.append(RayDoor(dist_adjusted, offset, door.is_vertical))
                if v.mag < self.__dist:
                    self.__dist = v.mag
                    self.__vector2d = v + pos
                    self.__dist_adjusted = dist_adjusted

    def cast_items(self, player, items: []):
        self.__items = []
        pos = Vector2d(player.x, player.y)
        if self.type_id is not None:
            for i in items:
                item: Item = i
                item_pos = (Vector2d(item.x, item.y) - pos)
                ray_pos = (self.__vector2d - pos)
                if item_pos.mag < ray_pos.mag:
                    ray_pos = ray_pos ** -self.ang
                    item_pos = item_pos ** -self.ang
                    if ray_pos.x < item_pos.x:
                        continue
                    if item_pos.y > 0.5 or item_pos.y < -0.5:
                        continue
                    dist = math.sin(math.pi / 2 - self.__rel_ang) * item_pos.x
                    self.__items.append(RayItem(item.type_id, dist, item_pos.y, item.get_state(player)))
                    
                

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

        self.__delta_dist_x = abs(
            1 / math.cos(self.ang)) if math.cos(self.ang) != 0 else math.inf
        self.__delta_dist_y = abs(
            1 / math.sin(self.ang)) if math.sin(self.ang) != 0 else math.inf

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


class RayItem():
    def __init__(self, type_id, dist, offset, state):
        self.__type_id = type_id
        self.__dist = dist
        self.__offset = offset
        self.__state = state

    @property
    def type_id(self):
        return self.__type_id

    @property
    def dist(self):
        return self.__dist

    @property
    def offset(self):
        return self.__offset

    @property
    def state(self):
        return self.__state

class RayDoor():
    def __init__(self, dist, offset, is_vertical):
        self.__type_id = 49
        self.__dist = dist
        self.__offset = offset
        self.__is_vertical = is_vertical

    @property
    def type_id(self):
        return self.__type_id

    @property
    def dist(self):
        return self.__dist

    @property
    def offset(self):
        return self.__offset

    @property
    def is_vertical(self):
        return self.__is_vertical

    @property
    def state(self):
        return 1 if self.is_vertical else 0
