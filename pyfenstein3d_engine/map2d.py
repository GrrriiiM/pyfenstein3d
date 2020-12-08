from .item import Item
from .wall import Wall
from .decoration import Decoration
from .item_grid import ItemGrid
from .player import Player


class Map2d():
    def __init__(self, items: []):
        self.__grid = ItemGrid(items)
        self.__players = { item.id: item for item in items if item is Player}

    @property
    def grid(self) -> Item:
        return self.__grid

    def update(self):
        for player in self.__players:
            player.update()

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
