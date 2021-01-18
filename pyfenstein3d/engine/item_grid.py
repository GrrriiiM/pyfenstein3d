import math
import numpy as np
from .item import Item
from .vector2d import Vector2d
from .decoration import Decoration
from .wall import Wall
from .door import Door
from .block import Block


class ItemGrid():
    def __init__(self, blocks: []):
        self.__max_x = max(map(lambda i: i.block_x, blocks)) + 1
        self.__max_y = max(map(lambda i: i.block_y, blocks)) + 1
        grid = [None] * self.__max_y * self.__max_x
        self.__items = []
        self.__doors = []
        self.__grid = np.asarray([grid[n:n+self.__max_y]
                                  for n in range(0, len(grid), self.__max_y)])
        for block in blocks:
            if isinstance(block, Item):
                self.__items.append(block)
            if isinstance(block, Door):
                self.__doors.append(block)
            if not block.is_moveable:
                self.__grid[block.block_x, block.block_y] = block

    def get_block(self, block_x, block_y) -> Item:
        block_x = math.floor(block_x)
        block_y = math.floor(block_y)
        if block_x < self.max_x and block_y < self.max_y:
            return self.__grid[block_x, block_y]
        return None

    def remove_block(self, block_x, block_y):
        block_x = math.floor(block_x)
        block_y = math.floor(block_y)
        self.__grid[block_x, block_y] = None

    def get_blocks_by_fov(self, pos: Vector2d, fov_ang: float, fov_delta: float, dist: float, type_block = Block):
        blocks = self.__grid
        fov_ang_vec_min = Vector2d.create_with_ang(fov_ang - (fov_delta * 0.5))
        fov_ang_vec_max = Vector2d.create_with_ang(fov_ang + (fov_delta * 0.5))
        if fov_ang_vec_min.x > 0 and fov_ang_vec_max.x > 0:
            blocks = blocks[math.floor(pos.x):, :]
        elif fov_ang_vec_min.x < 0 and fov_ang_vec_max.x < 0:
            blocks = blocks[:math.floor(pos.x+1), :]
        if fov_ang_vec_min.y > 0 and fov_ang_vec_max.y > 0:
            blocks = blocks[:, math.floor(pos.y):]
        elif fov_ang_vec_min.y < 0 and fov_ang_vec_max.y < 0:
            blocks = blocks[:, :math.floor(pos.y+1)]

        blocks = [block for line in blocks for block in line
                      if isinstance(block, type_block)]

        blocks = [block for block in blocks if block.is_in_fov(pos, fov_ang, fov_delta, dist)]
        
        return blocks
        
    def get_doors_by_fov(self, pos: Vector2d, fov_ang: float, fov_delta: float, dist: float):
        return self.get_blocks_by_fov(pos, fov_ang, fov_delta, dist, Door)

    def get_items_by_fov(self, pos: Vector2d, fov_ang: float, fov_delta: float, dist: float):
        return self.get_blocks_by_fov(pos, fov_ang, fov_delta, dist, Item)

    @property
    def max_x(self):
        return self.__max_x

    @property
    def max_y(self):
        return self.__max_y
