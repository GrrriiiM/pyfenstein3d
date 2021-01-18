from .item import Item
from .wall import Wall
from .decoration import Decoration
from .item_grid import ItemGrid
from .player import Player
from .person import Person
from .door import Door
from .item_weapon import ItemWeapon
from .item_ammo import ItemAmmo
from .item_score import ItemScore


class Map2d():
    def __init__(self, items: []):
        self.__grid = ItemGrid(items)
        self.__players = {item.player_id: item for item in items if isinstance(item, Player)}
        self.__persons = [item for item in items if isinstance(item, Person)]
        self.__doors = [item for item in items if isinstance(item, Door)]

    @property
    def grid(self) -> Item:
        return self.__grid

    def update(self, delta_time: float):
        for player_id in self.__players:
            player = self.__players[player_id]
            player.update(delta_time, self.__grid)
            player.adjust_collision(self.__grid)
            player.cast(self.__grid)
        for door in self.__doors:
            door.update(delta_time, self.__persons)


    def get_player(self, player_id: str):
        return self.__players[player_id]

    @staticmethod
    def create_with_pattern(pattern: str):
        items = []
        lines = pattern.splitlines()
        list_type_ids = [[s[n:n+2]
                          for n in range(0, len(s), 2)] for s in lines]
        for block_y, type_ids in enumerate(list_type_ids):
            for block_x, type_id_hex in enumerate(type_ids):
                if type_id_hex.strip() == "":
                    continue
                type_id = int(type_id_hex, 16)
                if type_id in type_ids_walls_solid:
                    items.append(Wall(block_x, block_y, type_id))
                elif type_id in type_ids_weapon:
                    items.append(ItemWeapon(block_x + 0.5, block_y + 0.5, type_id, False))
                elif type_id in type_ids_ammo:
                    items.append(ItemAmmo(block_x + 0.5, block_y + 0.5, type_id, False))
                elif type_id in type_ids_score:
                    items.append(ItemScore(block_x + 0.5, block_y + 0.5, type_id, False))
                elif type_id in type_ids_decorations_non_solid:
                    items.append(Decoration(block_x + 0.5, block_y + 0.5, type_id, False))
                elif type_id in type_ids_decorations_solid:
                    items.append(Decoration(block_x + 0.5, block_y + 0.5, type_id, True))
                elif type_id in type_ids_doors_horizontal:
                    items.append(Door(block_x, block_y + 0.5, type_id, False))
                elif type_id in type_ids_doors_vertical:
                    items.append(Door(block_x + 0.5, block_y, type_id, True))
                elif type_id in type_ids_player:
                    items.append(Player.create(block_x, block_y, type_id))
        return Map2d(items)



type_ids_decorations_solid = [57, 60, 61, 63, 65, 66, 68,
                         69, 70, 71, 74, 75, 76, 80, 93, 94, 95, 97]
# type_ids_decorations_non_solid = [58, 62, 67,
#                              72, 73, 77, 81, 92, 96, 99, 100, 101, 102]

type_ids_decorations_non_solid = [i for i in range(56,120) if i not in type_ids_decorations_solid]
type_ids_walls_solid = list(range(48)) + [53, 54]
type_ids_score = [ 87, 88, 89 ]
type_ids_weapon = [ 85, 86 ]
type_ids_ammo = [ 84 ]

type_ids_doors_horizontal = [50]
type_ids_doors_vertical = [49]
type_ids_player = [255]
