from pyfenstein3d.item import Item
from pyfenstein3d.wall import Wall
from pyfenstein3d.decoration import Decoration


class Map2d():
    def __init__(self, items: []):
        self.__max_x = max(map(lambda i: i.block_x, items)) + 1
        self.__max_y = max(map(lambda i: i.block_y, items)) + 1
        self.__items = []
        self.__walls = []
        self.__decorations = []
        blocks = [None] * self.__max_y * self.__max_x
        self.__blocks = [blocks[n:n+self.__max_y]
                         for n in range(0, len(blocks), self.__max_y)]
        for item in items:
            self.__items.append(item)
            if isinstance(item, Wall):
                self.__walls.append(item)
            if isinstance(item, Decoration):
                self.__decorations.append(item)
            self.__blocks[item.block_x][item.block_y] = item

    def block(self, block_x: int, block_y: int) -> Item:
        return self.__blocks[block_x][block_y] if self.__blocks[block_x] is not None else None

    @property
    def walls(self):
        return tuple(self.__walls)

    @property
    def max_x(self):
        return self.__max_x

    @property
    def max_y(self):
        return self.__max_y

    @staticmethod
    def create_with_pattern(pattern: str):
        items = []
        lines = pattern.splitlines()
        list_type_ids = [[s[n:n+2]
                          for n in range(0, len(s), 2)] for s in lines]
        for block_y, type_ids in enumerate(list_type_ids):
            for block_x, type_id_hex in enumerate(type_ids):
                if type_id_hex == "  ":
                    continue
                type_id = int(type_id_hex, 16)
                if type_id in walls_solid_type_ids:
                    items.append(Wall(block_x, block_y, type_id))
                elif type_id in decorations_non_solid_type_ids:
                    items.append(Decoration(block_x, block_y, type_id, False))
                elif type_id in decorations_solid_type_ids:
                    items.append(Decoration(block_x, block_y, type_id, True))
        return Map2d(items)

    @staticmethod
    def create_with_file(file_path: str):
        pattern: str
        with open(file_path, "r") as file:
            pattern = file.readlines()
        return Map2d.create_with_pattern(pattern)


decorations_non_solid_type_ids = [58, 62, 67,
                                  72, 73, 77, 81, 92, 96, 99, 100, 101, 102]
decorations_solid_type_ids = [57, 60, 61, 63, 65, 66, 68,
                              69, 70, 71, 74, 75, 76, 80, 93, 94, 95, 97]
walls_solid_type_ids = list(range(48))
doors_horizontal_type_ids = [49]
doors_vertical_type_ids = [50]
