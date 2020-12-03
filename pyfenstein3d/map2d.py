from pyfenstein3d.wall import Wall
from pyfenstein3d.decoration import Decoration

class Map2d():
    def __init__(self, items: []):
        self.__max_x = max(map(lambda i: i.block_x, items)) + 1
        self.__max_y = max(map(lambda i: i.block_y, items)) + 1
        self.__items = []
        self.__walls = []
        self.__decorations = []
        self.__blocks = [[None] * self.__max_y] * self.__max_x
        for item in items:
            self.__items.append(item)
            if isinstance(item, Wall): self.__walls.append(item) 
            if isinstance(item, Decoration): self.__decorations.append(item) 
            self.__blocks[item.block_x][item.block_y] = item

    def block(self, x: int, y: int):
        return self.__blocks[x][y] if self.__blocks[x] is not None else None

    @property
    def walls(self):
        return tuple(self.__walls)

    @property
    def max_x(self):
        return self.__max_x

    @property
    def max_y(self):
        return self.__max_y
        
