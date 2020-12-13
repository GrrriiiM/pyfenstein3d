import math
import numpy as np
from .item import Item
from .vector2d import Vector2d
from .decoration import Decoration


class ItemGrid():
    def __init__(self, items: []):
        self.__max_x = max(map(lambda i: i.block_x, items)) + 1
        self.__max_y = max(map(lambda i: i.block_y, items)) + 1
        grid = [None] * self.__max_y * self.__max_x
        self.__grid = np.asarray([grid[n:n+self.__max_y]
                                  for n in range(0, len(grid), self.__max_y)])
        for item in items:
            self.__grid[item.block_x, item.block_y] = item

    def get_item_by_block(self, block_x, block_y) -> Item:
        if block_x < self.max_x and block_y < self.max_y:
            return self.__grid[block_x, block_y]
        return None

    def get_items_by_fov(self, pos: Vector2d, ang: Vector2d, ang_min: Vector2d, ang_max: Vector2d):
        grid = self.__grid
        # if ang_min.x > 0 and ang_max.x > 0:
        #     grid = grid[math.floor(pos.x):, :]
        # elif ang_min.x < 0 and ang_max.x < 0:
        #     grid = grid[:math.floor(pos.x), :]
        # if ang_min.y > 0 and ang_max.y > 0:
        #     grid = grid[:, math.floor(pos.y):]
        # elif ang_min.y < 0 and ang_max.y < 0:
        #     grid = grid[:, :math.floor(pos.y)]

        items = []
        grid_items = [item for line in grid for item in line
                      if isinstance(item, Decoration)]

        ang_delta = ((ang_max.ang - ang_min.ang) + math.pi * 2) % (math.pi * 2)
        for grid_item in grid_items:
            grid_item_vector = (
                Vector2d(grid_item.x, grid_item.y) - pos) ** - ang.ang
            grid_item_ang_min = grid_item_vector.ang
            grid_item_ang_max = (grid_item_vector + Vector2d(0, 1)).ang
            if grid_item_ang_max > math.pi:
                grid_item_ang_max -= math.pi * 2
            if grid_item_ang_min > math.pi:
                grid_item_ang_min -= math.pi * 2
            if grid_item_ang_max >= ang_delta * -0.5 and grid_item_ang_min <= ang_delta * 0.5:
                items.append(grid_item)

        return items

        #     let pos = this.pos.copy();
        #     pos.sub(view.person.pos);
        #     pos.rotate(-view.angle);
        #     if (pos.x <= 0) return false;
        #     let itemAngleMin = pos.ang;
        #     pos.y += 1;
        #     let itemAngleMax = pos.ang;
        #     if (itemAngleMin <= view.angleTotal * 0.5 && view.angleTotal * -0.5 <= itemAngleMax) {
        #         return true;
        #     } else {
        #         return false;
        #     }

    @property
    def max_x(self):
        return self.__max_x

    @property
    def max_y(self):
        return self.__max_y
